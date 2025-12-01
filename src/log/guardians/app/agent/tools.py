import subprocess
import os
import yaml
import json
from typing import Dict, Any, List
from collections import Counter
from src.log.guardians.app.main.main import load_config, chunk_log_file
from src.log.guardians.app.utils.json_cleaner import clean_json_content

def run_log_generator() -> str:
    """Runs the main log generation script to create fresh logs."""
    try:
        # Using the absolute path or relative from project root
        config = load_config('src/log/guardians/app/main/config/chunker_config.yaml')
        chunk_log_file(config)

        return f"Log generation completed."
    except Exception as e:
        return f"Log generation failed.\nError: {e}"


def structure_architect_tool(config_path: str = "src/log/guardians/app/main/config/chunker_config.yaml") -> Dict[str, Any]:
    """Analyzes config and sample log to design schema."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Read dynamic values from config
        active_profile = config.get('active_profile')
        sample_log_path = config.get('input_log_file')
        regex_pattern = config['log_profiles'][active_profile]['log_start_regex']

        with open(sample_log_path, 'r', errors='replace') as f:
            sample_lines = [next(f) for _ in range(20)]

        return {
            "regex_pattern": regex_pattern,
            "sample_content": "".join(sample_lines),
            "profile_description": config['log_profiles'][active_profile]['description']
        }
    except Exception as e:
        return {"error": str(e)}


def get_log_files_tool(config_path: str = "src/log/guardians/app/main/config/chunker_config.yaml") -> List[str]:
    """Returns a list of all log files in the directory."""

    # Read config to get dynamic path
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    active_profile = config.get('active_profile')
    log_file_name = config.get('input_log_file').split('/')[-1].replace('.log', '')

    # Build path: .LogGuardians/output/logs/{profile}/{log_file_name}/
    log_dir = f".LogGuardians/output/logs/{active_profile}/{log_file_name}"

    abs_log_dir = os.path.abspath(log_dir)
    log_files = []
    for root, _, files in os.walk(abs_log_dir):
        for file in files:
            if file.endswith(".log"):
                log_files.append(os.path.join(root, file))
    return sorted(log_files)

def read_file_tool(file_path: str) -> str:
    """Reads the content of a specific log file."""
    try:
        with open(file_path, 'r', errors='replace') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


def save_json_tool(data: list, original_file_path: str, schema_keys: list = None) -> str:
    """Saves the structured JSON data."""

    filename = os.path.basename(original_file_path).replace(".log", ".json")
    output_dir = os.path.abspath(".LogGuardians/output_json_structured_logs")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    try:
        if isinstance(data, str):
            cleaned_data = clean_json_content(data)
            data = json.loads(cleaned_data)
            
        final_data = data
        if schema_keys:
            # Enforce dynamic key order
            ordered_data = []
            for entry in data:
                ordered_entry = {k: entry.get(k) for k in schema_keys if k in entry}
                # Add any other keys that might be present
                for k, v in entry.items():
                    if k not in schema_keys:
                        ordered_entry[k] = v
                ordered_data.append(ordered_entry)
            final_data = ordered_data

        with open(output_path, 'w') as f:
            json.dump(final_data, f, indent=2)
        return f"Saved to {output_path}"
    except Exception as e:
        return {"error": str(e)}

def read_json_file_tool(file_path: str) -> Dict[str, Any]:
    """Reads a specific JSON file and returns its content."""

    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        return {"error": f"Error reading file: {str(e)}"}

def get_json_files_tool(json_dir: str = ".LogGuardians/output_json_structured_logs") -> List[str]:
    """Returns a list of all JSON files in the directory."""
    abs_dir = os.path.abspath(json_dir)
    json_files = []
    for root, _, files in os.walk(abs_dir):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return sorted(json_files)

def save_anomaly_json_tool(data: Dict[str, Any], original_filename: str) -> str:
    """Saves the anomaly report to a JSON file."""
    from datetime import datetime

    # Create output directory
    output_dir = os.path.abspath(".LogGuardians/output_anomalies")
    os.makedirs(output_dir, exist_ok=True)

    # Construct filename: chunk_0000_anomaly.json
    base_name = os.path.basename(original_filename).replace(".json", "")
    filename = f"{base_name}_anomaly.json"
    output_path = os.path.join(output_dir, filename)

    # Add metadata
    # Add metadata
    try:
        if isinstance(data, str):
            cleaned_data = clean_json_content(data)
            data = json.loads(cleaned_data)
    except Exception as e:
        return {"error": f"Error parsing anomaly JSON: {str(e)}"}

    data["file"] = original_filename
    data["timestamp_analyzed"] = datetime.now().isoformat()

    try:
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        return f"Saved anomaly report to {output_path}"
    except Exception as e:
        return {"error": f"Error saving anomaly file: {str(e)}"}
