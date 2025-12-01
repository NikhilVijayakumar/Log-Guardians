import asyncio
import sys
import os
import json
from typing import Dict, List, Any

# Ensure we can import modules from src when running from project root
sys.path.append(os.getcwd())
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types
from src.log.guardians.app.agent.tools import read_json_file_tool, get_json_files_tool

load_dotenv()

# --- Agent Configuration ---

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

model = Gemini(
    model="gemini-2.5-flash",
    retry_options=retry_config
)

agent = Agent(
    name="ReportGenerator",
    model=model,
    description="An AI agent that aggregates anomaly reports and generates a consolidated security summary.",
    instruction="""
    You are an expert Security Analyst. Your goal is to generate a **Consolidated Security Report** based on a list of detected anomalies.

    **Input Data**:
    - You will receive a JSON object containing a list of anomalies from multiple log files.

    **Your Task**:
    1.  **Analyze the Aggregated Data**:
        - Identify the most critical issues across all files.
        - Group anomalies by **Severity** (Critical, High, Medium, Low).
        - Look for **patterns** (e.g., is the same IP attacking multiple nodes? Is a specific service failing repeatedly?).

    2.  **Generate Markdown Report**:
        - Create a professional, structured Markdown report.
        - **Structure**:
            - **Executive Summary**: High-level overview of the system's security posture.
            - **Critical Threats**: Detailed analysis of the most severe issues.
            - **Pattern Analysis**: Insights into recurring attacks or failures.
            - **Detailed Findings by Severity**: Grouped list of anomalies.
            - **Actionable Recommendations**: Prioritized steps to mitigate risks.

    **Output Format**:
    - Return ONLY the Markdown content.
    """,
    tools=[] # No tools needed for the LLM itself, we pass data in context
)

runner = InMemoryRunner(agent=agent)


async def run_report_generation():
    """Runs the report generation pipeline."""
    print("=" * 60)
    print("📊 REPORT GENERATOR AGENT")
    print("=" * 60)
    print("\nInitializing report generation...\n")

    try:
        # 1. Get List of Anomaly Files
        anomaly_dir = ".LogGuardians/output_anomalies"
        print(f"Step 1: Reading anomaly files from {anomaly_dir}...")

        # We can reuse get_json_files_tool by passing the directory
        anomaly_files = get_json_files_tool(anomaly_dir)

        if not anomaly_files:
            print("No anomaly files found. System appears healthy.")
            return

        print(f"Found {len(anomaly_files)} anomaly reports.")

        # 2. Aggregate Data
        print("\nStep 2: Aggregating data...")
        aggregated_anomalies = []

        for file_path in anomaly_files:
            try:
                data = read_json_file_tool(file_path)
                if "anomalies" in data:
                    # Add filename context to each anomaly if not present
                    for anomaly in data["anomalies"]:
                        anomaly["source_file"] = os.path.basename(file_path)
                    aggregated_anomalies.extend(data["anomalies"])
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

        print(f"Total anomalies found: {len(aggregated_anomalies)}")

        # 3. Generate Report
        print("\nStep 3: Generating consolidated report...")

        # Prepare context for the agent
        context_data = json.dumps(aggregated_anomalies, indent=2)

        # Run the agent
        response = await runner.run_debug(
            f"Here is the aggregated anomaly data:\n\n{context_data}\n\nGenerate the Consolidated Security Report."
        )

        # Extract response
        last_turn = response[-1]
        if hasattr(last_turn, 'content') and last_turn.content and last_turn.content.parts:
            report_content = last_turn.content.parts[0].text
        else:
            report_content = str(last_turn)

        # 4. Save Report
        output_file = "FINAL_ANOMALY_REPORT.md"
        with open(output_file, "w") as f:
            f.write(report_content)

        print(f"\n✅ Report saved to: {os.path.abspath(output_file)}")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
        raise

async def main():
    """Entry point when running as standalone script."""
    await run_report_generation()

if __name__ == "__main__":
    asyncio.run(main())

