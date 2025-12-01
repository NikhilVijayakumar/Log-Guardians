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
from fastapi import FastAPI, HTTPException

# Ensure we can import modules from src when running from project root
sys.path.append(os.getcwd())

from src.log.guardians.app.features.chunking.chunker import load_config, chunk_log_file

app = FastAPI(title="Log Guardians Pipeline", description="Single Endpoint API for Log Analysis")

async def run_pipeline_logic():
    """
    Executes the complete log analysis pipeline logic.
    Returns a summary or report content.
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
        try:
            from src.log.guardians.app.agent.json_converter_agent import run_conversion
            await run_conversion()
            print("✅ JSON conversion completed.")
        except ImportError:
            print("⚠️ JSON Converter Agent not available.")

        # Step 3: Detect Anomalies
        print("\n🔍 STEP 3: Detecting Anomalies...")
        print("-" * 80)
        try:
            from src.log.guardians.app.agent.anomaly_detection_agent import run_anomaly_detection
            await run_anomaly_detection()
            print("✅ Anomaly detection completed.")
        except ImportError:
            print("⚠️ Anomaly Detection Agent not available.")

        # Step 4: Generate Report
        print("\n📊 STEP 4: Generating Consolidated Report...")
        print("-" * 80)
        report_content = "Report generation failed or skipped."
        try:
            from src.log.guardians.app.agent.report_generator_agent import run_report_generation
            await run_report_generation()
            print("✅ Report generation completed.")
            
            # Read the generated report
            report_path = "FINAL_ANOMALY_REPORT.md"
            if os.path.exists(report_path):
                with open(report_path, "r") as f:
                    report_content = f.read()
            else:
                report_content = "Report generated but file not found."
        except ImportError:
            print("⚠️ Report Generator Agent not available.")

        print("\n" + "=" * 80)
        print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
        return {"status": "success", "report": report_content}

    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        raise e

@app.post("/api/run-pipeline")
async def run_pipeline_endpoint():
    try:
        result = await run_pipeline_logic()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def main():
    """Entry point for running as script."""
    asyncio.run(run_pipeline_logic())

if __name__ == "__main__":
    main()