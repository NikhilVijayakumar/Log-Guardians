import os
import re
import yaml
import sys
from datetime import datetime

def load_config(config_path='config/chunker_config.yaml'):
    """Loads the YAML configuration file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print(f"✅ Configuration loaded from {config_path}")
        return config
    except FileNotFoundError:
        print(f"❌ ERROR: Configuration file not found at {config_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ ERROR: Failed to parse YAML file: {e}")
        sys.exit(1)


def write_chunk_to_file(lines, output_dir, chunk_num):
    """Writes a list of lines to a new chunk file."""
    chunk_file_path = os.path.join(output_dir, f"chunk_{chunk_num:04d}.log")
    try:
        with open(chunk_file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"💾 Wrote chunk {chunk_num} -> {chunk_file_path} ({len(lines)} lines)")
        return chunk_file_path
    except IOError as e:
        print(f"❌ ERROR: Could not write chunk file {chunk_file_path}: {e}")
        return None


def chunk_log_file(config):
    """
    Reads the large log file and splits it into chunks based on
    the rules in the config.
    """
    # --- 1. Get settings from config ---
    try:
        input_file = config['input_log_file']
        base_output_dir = config['output_chunk_dir']
        active_profile_name = config['active_profile']
        input_basename = os.path.splitext(os.path.basename(input_file))[0]
        output_dir = os.path.join(base_output_dir, active_profile_name, input_basename)
        max_entries = int(config.get('max_entries_per_chunk', 500))


        if active_profile_name not in config['log_profiles']:
            print(f"❌ ERROR: Active profile '{active_profile_name}' not found in 'log_profiles' section.")
            print("Available profiles are:")
            for key in config['log_profiles']:
                print(f"  - {key}")
            sys.exit(1)

        profile = config['log_profiles'][active_profile_name]
        log_start_regex = profile['log_start_regex']

        print(f"ℹ️  Active profile: '{active_profile_name}' ({profile.get('description', 'No description')})")

    except KeyError as e:
        print(f"❌ ERROR: Config file is missing required key: {e}")
        sys.exit(1)

    # --- 2. Compile regex and create output dir ---
    try:
        # Use multiline and ignorecase not necessary, but compile plainly
        start_pattern = re.compile(log_start_regex)
    except re.error as e:
        print(f"❌ ERROR: Invalid regex in profile '{active_profile_name}': {e}")
        sys.exit(1)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"📁 Created output directory: {output_dir}")
    else:
        # Clean out old chunks
        print("🧹 Cleaning old chunks from output directory...")
        for f in os.listdir(output_dir):
            if f.startswith("chunk_") and f.endswith(".log"):
                try:
                    os.remove(os.path.join(output_dir, f))
                except Exception:
                    pass

    # --- 3. Process the file (memory-efficient) ---
    if not os.path.isfile(input_file):
        print(f"❌ ERROR: Input log file not found at {input_file}")
        sys.exit(1)

    print(f"🚀 Starting to process {input_file}...")
    chunk_num = 0
    entry_count = 0
    current_chunk_lines = []
    chunk_files_created = []

    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            for lineno, line in enumerate(f, start=1):
                if start_pattern.match(line):
                    # This line is the start of a new log entry.
                    # If current entry_count already at max, flush the chunk.
                    if entry_count >= max_entries:
                        path = write_chunk_to_file(current_chunk_lines, output_dir, chunk_num)
                        if path:
                            chunk_files_created.append(path)
                        chunk_num += 1
                        current_chunk_lines = [line]
                        entry_count = 1
                        print(f"🔹 New chunk started at line {lineno} (chunk {chunk_num})")
                    else:
                        # New entry but not exceeding chunk size: append as new entry
                        current_chunk_lines.append(line)
                        entry_count += 1
                        # For first matched line after startup, show debug
                        if entry_count == 1 and len(current_chunk_lines) == 1:
                            print(f"🔸 First log entry detected at line {lineno}")
                else:
                    # Continuation line (stacktrace, wrapped line, etc.)
                    if current_chunk_lines:
                        current_chunk_lines.append(line)
                    else:
                        # line that doesn't match and we haven't started a chunk yet;
                        # optionally write it to an "orphan" chunk or ignore
                        # We'll start collecting only once we see the first matching start line.
                        continue

            # --- 4. Write the final remaining chunk ---
            if current_chunk_lines:
                path = write_chunk_to_file(current_chunk_lines, output_dir, chunk_num)
                if path:
                    chunk_files_created.append(path)

    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        sys.exit(1)

    print("\n🎉 --- Chunking Complete! ---")
    print(f"Total chunk files created: {len(chunk_files_created)}")
    print(f"Chunks saved in: {os.path.abspath(output_dir)}")

    return chunk_files_created



