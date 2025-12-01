import sys
import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from src.log.guardians.app.agent.tools import run_log_generator
from src.log.guardians.app.utils.json_cleaner import clean_json_content

# Ensure we can import modules from src when running from project root
sys.path.append(os.getcwd())
# Also add the directory containing this script to path to find tools.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from google.adk.agents import Agent

load_dotenv()
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types
from src.log.guardians.app.agent.tools import run_log_generator

retry_config=types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

root_agent = Agent(
    name="LogGenerator",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    description="You are the Log Generator. Your task is to generate logs.",
    instruction="You are the Log Generator. Your task is to generate logs.Dont include any thing extra just execute the the tool for generating the logs.",
    tools=[run_log_generator],
)

runner = InMemoryRunner(agent=root_agent)


async def main():
    response = await runner.run_debug(
        "Generate the logs for the HPC."
    )
    print(clean_json_content(response[-1].content.parts[0].text))

if __name__ == "__main__":
    asyncio.run(main())
