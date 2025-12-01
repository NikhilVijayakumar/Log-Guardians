"""
Log Guardians Pipeline Orchestrator

This module orchestrates the complete log analysis pipeline:
1. Generate/Chunk logs
2. Convert logs to structured JSON
3. Detect anomalies
4. Generate consolidated report
"""

import asyncio
import sys
import os

# Ensure we can import modules from src when running from project root
sys.path.append(os.getcwd())

from src.log.guardians.app.features.chunking.chunker import load_config, chunk_log_file


async def run_pipeline():
    """
    Executes the complete log analysis pipeline.
    """
    print("=" * 80)
    print("🚀 LOG GUARDIANS PIPELINE")
    print("=" * 80)

    try:
        # Step 1: Generate and Chunk Logs
        print("\n📝 STEP 1: Generating and Chunking Logs...")
        print("-" * 80)
        config = load_config('src/log/guardians/app/main/config/chunker_config.yaml')
        chunk_log_file(config)
        print("✅ Log chunking completed.")

        # Step 2: Convert Logs to JSON
        print("\n🔄 STEP 2: Converting Logs to Structured JSON...")
        print("-" * 80)
        from src.log.guardians.app.agent.json_converter_agent import run_conversion
        await run_conversion()
        print("✅ JSON conversion completed.")

        # Step 3: Detect Anomalies
        print("\n🔍 STEP 3: Detecting Anomalies...")
        print("-" * 80)
        from src.log.guardians.app.agent.anomaly_detection_agent import run_anomaly_detection
        await run_anomaly_detection()
        print("✅ Anomaly detection completed.")

        # Step 4: Generate Report
        print("\n📊 STEP 4: Generating Consolidated Report...")
        print("-" * 80)
        from src.log.guardians.app.agent.report_generator_agent import run_report_generation
        await run_report_generation()
        print("✅ Report generation completed.")

        print("\n" + "=" * 80)
        print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\n📄 Check FINAL_ANOMALY_REPORT.md for the security analysis.")

    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Entry point for the pipeline."""
    asyncio.run(run_pipeline())


if __name__ == "__main__":
    main()