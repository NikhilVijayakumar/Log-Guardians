import pathlib
import sys
from typing import List, Optional


def find_log_files(folder_path_str: str) -> List[pathlib.Path]:
    """
    Scans a directory and returns a list of Path objects for all .log files.

    Args:
        folder_path_str: The string path to the folder


    Returns:
        A list of pathlib.Path objects, one for each .log file found.
        Returns an empty list if the directory is not found or no files match.
    """
    # Use pathlib.Path to handle the path (works for Windows, Mac, Linux)
    folder_path = pathlib.Path(folder_path_str)

    # Check if the path is a valid directory
    if not folder_path.is_dir():
        print(f"❌ Error: Directory not found at {folder_path_str}", file=sys.stderr)
        return []

    print(f"Scanning for .log files in: {folder_path}\n")

    # Use .glob() to find all files ending in .log
    log_files = list(folder_path.glob('*.log'))

    if not log_files:
        print("No .log files found.")
    else:
        print(f"Found {len(log_files)} log files.")

    return log_files


def read_file_as_string(file_path: pathlib.Path) -> Optional[str]:
    """
    Reads the entire content of a single file into one string.

    Args:
        file_path: A pathlib.Path object pointing to the file.

    Returns:
        The content of the file as a single string, or None if
        an error occurs.
    """
    try:
        # read_text handles opening, reading, and closing the file.
        # errors='ignore' is robust for log files that might
        # have non-UTF-8 characters.
        return file_path.read_text(encoding='utf-8', errors='ignore')
    except FileNotFoundError:
        print(f"❌ Error: File not found {file_path}", file=sys.stderr)
        return None
    except IOError as e:
        print(f"❌ Error reading file {file_path}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ An unexpected error occurred with {file_path}: {e}", file=sys.stderr)
        return None

