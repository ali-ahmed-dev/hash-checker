"""
Hash Checker - A tool for calculating and verifying file hashes.
"""


from datetime import datetime
from typing import Optional
from pathlib import Path
import hashlib
import json

# ===================== CONSTANTS =====================
CHUNK_SIZE = 4096  # Default chunk size for reading files (adjust for performance)
SEPARATOR = "=" * 50

HEADER = f"{SEPARATOR}\n                 HASH CHECKER \n{SEPARATOR}"
FOOTER = f"{SEPARATOR}\n                 END OF REPORT\n{SEPARATOR}"

SUPPORTED_ALGORITHMS = {
    "1": "md5",
    "2": "sha1",
    "3": "sha256",
    "4": "sha512",
}


# ===================== CORE FUNCTIONS =====================
def calculate_hash(file_path: Path, algorithm: str) -> str:
    """
    Calculate the hash of a file using the specified algorithm.

    Args:
        file_path (Path): Path to the file.
        algorithm (str): Hashing algorithm (e.g., 'md5', 'sha256').

    Returns:
        str: Hexadecimal hash digest.
    """
    hash_obj = hashlib.new(algorithm)
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(CHUNK_SIZE), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def compare_hashes(expected: str, calculated: str) -> bool:
    """
    Compare expected hash with calculated hash (case-insensitive, trimmed).

    Args:
        expected (str): Expected hash value.
        calculated (str): Calculated hash value.

    Returns:
        bool: True if hashes match, False otherwise.
    """
    return expected.strip().lower() == calculated.lower()


# ===================== REPORT GENERATION =====================
def build_report(
    file_name: str,
    algorithm: str,
    calculated: str,
    expected: str,
    status: str,
    generated_at: str
) -> str:
    """
    Build a formatted report string.

    Args:
        file_name (str): Name of the analyzed file.
        algorithm (str): Hashing algorithm used.
        calculated (str): Calculated hash.
        expected (str): Expected hash.
        status (str): Comparison status.
        generated_at (str): Timestamp of report generation.

    Returns:
        str: Formatted report.
    """
    report = [
        HEADER,
        f"Generated   : {generated_at}",
        f"File Name   : {file_name}",
        f"Algorithm   : {algorithm.upper()}",
        f"Status      : {status}",
        f"Calculated  : {calculated}",
        f"Expected    : {expected}",
        FOOTER
    ]
    return "\n".join(report)


# ===================== EXPORT FUNCTIONS =====================
def get_timestamp() -> str:
    """Generate a timestamp string for filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def export_report_txt(report: str, file_name: str) -> None:
    """
    Export the report to a timestamped TXT file.

    Args:
        report (str): Report text to export.
        file_name (str): Original file name for naming the report.
    """
    timestamp = get_timestamp()
    txt_filename = f"{Path(file_name).stem}_report_{timestamp}.txt"
    Path(txt_filename).write_text(report, encoding="utf-8")
    print(f"Report exported to {txt_filename}")


def export_report_json(
    file_name: str,
    algorithm: str,
    calculated: str,
    expected: str,
    status: str,
    generated_at: str
) -> None:
    """
    Export report data to a timestamped JSON file.

    Args:
        file_name (str): Original file name.
        algorithm (str): Hashing algorithm used.
        calculated (str): Calculated hash.
        expected (str): Expected hash.
        status (str): Comparison status.
        generated_at (str): Timestamp of report generation.
    """
    timestamp = get_timestamp()
    json_filename = f"{Path(file_name).stem}_report_{timestamp}.json"

    report_data = {
        "generated_at": generated_at,
        "file_name": file_name,
        "algorithm": algorithm.upper(),
        "calculated_hash": calculated,
        "expected_hash": expected,
        "status": status
    }

    Path(json_filename).write_text(
        json.dumps(report_data, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"Report exported to {json_filename}")


# ===================== MAIN =====================
def main() -> None:
    """
    Main entry point for the Hash Checker tool.
    """
    print("Welcome to the Hash Checker Tool")

    user_input = input("Enter the file path: ").strip()
    if not user_input:
        print("Status: No file path provided.")
        return

    file_path = Path(user_input)
    if not file_path.exists():
        print(f"Error: file '{file_path}' not found.")
        return

    if not file_path.is_file():
        print(f"Error: '{file_path}' is a directory, not a file.")
        return

    print("Choose hash algorithm:\n1. MD5\n2. SHA1\n3. SHA256\n4. SHA512")
    algorithm_num = input("Choose an option (1-4): ").strip()

    if algorithm_num not in SUPPORTED_ALGORITHMS:
        print("Error: Invalid algorithm selection. Please choose a number between 1 and 4.")
        return

    algorithm = SUPPORTED_ALGORITHMS[algorithm_num]

    try:
        calculated = calculate_hash(file_path, algorithm)
    except (PermissionError, OSError) as e:
        print(f"Error reading file: {e}")
        return

    expected = input("Enter the hash to compare: ").strip()
    if not expected:
        print("Status: No hash provided for comparison.")
        return

    status = "Hashes Match" if compare_hashes(expected, calculated) else "Hashes Mismatch"
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = build_report(file_path.name, algorithm, calculated, expected, status, generated_at)
    print(report)

    export_report_txt(report, file_path.name)
    export_report_json(file_path.name, algorithm, calculated, expected, status, generated_at)


if __name__ == "__main__":
    main()