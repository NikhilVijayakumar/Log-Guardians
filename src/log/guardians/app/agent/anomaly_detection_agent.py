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
from src.log.guardians.app.agent.tools import read_json_file_tool, get_json_files_tool, save_anomaly_json_tool

load_dotenv()

# --- Agent Configuration ---

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

model = Gemini(
    model="gemini-2.5-flash-lite", 
    retry_options=retry_config
)

agent = Agent(
    name="AnomalyDetector",
    model=model,
    description="An AI agent specialized in detecting anomalies in structured log data.",
    instruction="""
    You are an expert Anomaly Detection Agent. Your goal is to analyze a SINGLE structured JSON log file and identify security threats, system failures, and unusual patterns using your own reasoning.

    **Your workflow:**

    1.  **Analyze Data**:
        - You will be provided with the content of a JSON log file in the prompt or via `read_json_file_tool`.
        - Read through the log entries carefully.
        - Look for patterns such as:
            - **Security Threats**: Repeated authentication failures, unauthorized access attempts (sudo/su), suspicious IP addresses.
            - **System Failures**: Critical errors, service crashes, hardware warnings.
            - **Anomalous Behavior**: Unusual time spikes, high frequency of specific events.
        - Use your broad knowledge of computer systems, applications, network protocols, and security to interpret the logs, regardless of the platform (Linux, Windows, Cloud, etc.).

    2.  **Report Findings**:
        - **CRITICAL**: Only report ACTUAL anomalies. Do not report normal system operations.
        - If NO anomalies are found, simply output: "No anomalies found." **DO NOT call the save tool.**
        - If anomalies ARE found, you MUST save them using `save_anomaly_json_tool`.
        - **Data Structure for Tool**:
            - `anomalies`: A list of anomaly objects, each containing:
                - `severity`: "Critical", "High", "Medium", or "Low".
                - `description`: What happened?
                - `evidence`: Specific log messages or patterns.
                - `correlation`: Connection between events.

    **Output Format**:
    - If anomalies found: "Anomalies detected and saved to JSON."
    - If no anomalies: "No anomalies found."
    """,
    tools=[read_json_file_tool, save_anomaly_json_tool]
)

runner = InMemoryRunner(agent=agent)


async def run_anomaly_detection():
    """Runs the anomaly detection pipeline."""
    print("=" * 60)
    print("🔍 LOG ANOMALY DETECTION AGENT (Iterative JSON Mode)")
    print("=" * 60)
    print("\nInitializing analysis...\n")

    try:
        # 1. Get List of JSON Files
        print("Step 1: Getting list of JSON files...")
        json_files = get_json_files_tool()
        print(f"Found {len(json_files)} JSON files to analyze.")

        if not json_files:
            print("No JSON files found. Exiting.")
            return

        # 2. Iterate and Analyze
        print("\nStep 2: Analyzing files...")

        anomalies_found_count = 0

        for i, file_path in enumerate(json_files):
            filename = os.path.basename(file_path)
            print(f"\n[{i+1}/{len(json_files)}] Analyzing: {filename}")

            # Run the agent for this specific file
            response = await runner.run_debug(
                f"Analyze this JSON log file: {file_path}. Original filename is '{filename}'. Read it using `read_json_file_tool`. If anomalies are found, save them using `save_anomaly_json_tool`."
            )

            # Extract response
            last_turn = response[-1]
            if hasattr(last_turn, 'content') and last_turn.content and last_turn.content.parts:
                agent_text = last_turn.content.parts[0].text
            else:
                agent_text = str(last_turn)

            # Check if anomalies were found
            if "No anomalies found" not in agent_text:
                print(f"⚠️  Anomalies detected in {filename}!")
                print(f"Agent Response: {agent_text}")
                anomalies_found_count += 1
            else:
                print(f"✅ No anomalies found in {filename}.")

            # Break after processing 5 files for testing
            if i >=5:
                break

        print("\n" + "=" * 60)
        print(f"Analysis Complete. Found anomalies in {anomalies_found_count} files.")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
        raise

async def main():
    """Entry point when running as standalone script."""
    await run_anomaly_detection()

if __name__ == "__main__":
    asyncio.run(main())

