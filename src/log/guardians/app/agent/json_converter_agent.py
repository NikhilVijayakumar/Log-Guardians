import asyncio
import sys
import os
import yaml
import json
from typing import Dict, Any, List

# Ensure we can import modules from src when running from project root
sys.path.append(os.getcwd())

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types
from src.log.guardians.app.agent.tools import structure_architect_tool, read_file_tool, save_json_tool, get_log_files_tool, run_log_generator

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
    name="LogProcessor",
    model=model,
    description="Processes log files to convert them to JSON.",
    instruction="""
    You are the Log Processor. Your task is to convert log files to JSON with **high precision**.

    **Capabilities:**
    1.  **Run Log Generator**: Run log generator to generate logs.
    2.  **Design Schema**: Analyze config/sample log file to design a JSON schema which will be best structured for finding anomalies in the log.
    3.  **Process File**: Read a specific file, parse it using the schema, and save it.

    **Important Rules for Processing:**
    *   **ACCURACY IS PARAMOUNT**: Do not summarize, truncate, or alter the data.
    *   **Message Field**: The `message` field must contain the **exact** text from the log, preserving all whitespace and special characters.
    *   **Field Order**: The output JSON should have the fields in this specific order and same for all entries:


    **Important:**
    *   When asked to "Design Schema", use `structure_architect_tool`.
    *   When asked to "Process File", use `read_file_tool` then `save_json_tool`.
    *   **Dynamic Ordering**: When calling `save_json_tool`, you MUST pass the list of keys from your designed schema as the `schema_keys` argument. This ensures the JSON output follows your designed structure.
    """,
    tools=[run_log_generator,structure_architect_tool, read_file_tool, save_json_tool]
)

runner = InMemoryRunner(agent=agent)


async def run_conversion():
    """Runs the JSON conversion pipeline."""
    print("--- JSON Conversion Started ---")
    try:
        # 1. Design Schema (Warm-up)
        print("\nStep 1: Designing Schema...")
        await runner.run_debug("Design the JSON schema for the logs.")

        # 2. Get File List (Directly in Python for efficiency)
        print("\nStep 2: Getting File List...")
        files = get_log_files_tool()
        print(f"Found {len(files)} files.")

        # 3. Loop through files
        print("\nStep 3: Processing Files...")
        for i, file_path in enumerate(files):
            print(f"Processing file {i+1}/{len(files)}: {os.path.basename(file_path)}")

            # Invoke Agent for this specific file
            await runner.run_debug(
                f"Process this log file: {file_path}. Read it, parse it using the schema, and save it."
            )

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()
        raise

async def main():
    """Entry point when running as standalone script."""
    await run_conversion()

if __name__ == "__main__":
    asyncio.run(main())

