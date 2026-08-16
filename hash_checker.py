"""
Hash Checker - A tool for calculating and verifying file hashes.
"""

from datetime import datetime
from pathlib import Path
import argparse
import hashlib
import json


# ===================== CONSTANTS =====================
CHUNK_SIZE = 4096  # Default chunk size for reading files (adjust for performance)
SEPARATOR = "=" * 50

HEADER = f"{SEPARATOR}\n                 HASH CHECKER \n{SEPARATOR}"
FOOTER = f"{SEPARATOR}\n                 END OF REPORT\n{SEPARATOR}"

SUPPORTED_ALGORITHMS = ["md5", "sha1", "sha256", "sha512"]


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


def export_report_txt(report: str, file_name: str, output_dir: Path = None) -> None:
    """
    Export the report to a timestamped TXT file.

    Args:
        report (str): Report text to export.
        file_name (str): Original file name for naming the report.
        output_dir (Path, optional): Directory to save the report.
    """
    if output_dir is None:
        output_dir = Path.cwd()

    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = get_timestamp()
    txt_filename = f"{Path(file_name).stem}_report_{timestamp}.txt"
    report_path = output_dir / txt_filename

    try:
        report_path.write_text(report, encoding="utf-8")
        print(f"Report exported to {report_path}")
    except (PermissionError, OSError) as e:
        print(f"Error: Could not write TXT report to {report_path}. {e}")


def export_report_json(
    file_name: str,
    algorithm: str,
    calculated: str,
    expected: str,
    status: str,
    generated_at: str,
    output_dir: Path = None
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
        output_dir (Path, optional): Directory to save the report.
    """
    if output_dir is None:
        output_dir = Path.cwd()

    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = get_timestamp()
    json_filename = f"{Path(file_name).stem}_report_{timestamp}.json"
    report_path = output_dir / json_filename

    report_data = {
        "generated_at": generated_at,
        "file_name": file_name,
        "algorithm": algorithm.upper(),
        "calculated_hash": calculated,
        "expected_hash": expected,
        "status": status
    }

    try:
        report_path.write_text(
            json.dumps(report_data, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )
        print(f"Report exported to {report_path}")
    except (PermissionError, OSError) as e:
        print(f"Error: Could not write JSON report to {report_path}. {e}")


# ===================== MAIN =====================
def main() -> None:
    """
    Main entry point for the Hash Checker tool (CLI version).
    """
    parser = argparse.ArgumentParser(
        description="Calculate and verify file hashes using multiple algorithms.",
        epilog="""
Examples:
  %(prog)s firmware.bin -a sha256
  %(prog)s firmware.bin -a sha256 -e 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
  %(prog)s firmware.bin -a md5 -o ./reports
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "file",
        help="Path to the file to hash"
    )

    parser.add_argument(
        "-a", "--algorithm",
        choices=SUPPORTED_ALGORITHMS,
        default="sha256",
        help=f"Hashing algorithm to use. Choices: {', '.join(SUPPORTED_ALGORITHMS)} (default: sha256)"
    )

    parser.add_argument(
        "-e", "--expected",
        help="Expected hash value to compare against"
    )

    parser.add_argument(
        "-o", "--output",
        help="Directory to save reports (default: current directory)"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress all output except errors and report messages"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print detailed progress during processing"
    )

    args = parser.parse_args()

    # Validate file path
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File '{args.file}' not found.")
        return

    if not file_path.is_file():
        print(f"Error: '{args.file}' is a directory, not a file.")
        return

    # Determine output directory
    output_dir = Path(args.output) if args.output else Path.cwd()

    # Create output directory if it doesn't exist
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except (PermissionError, OSError) as e:
        print(f"Error: Could not create output directory '{output_dir}'. {e}")
        return

    # Calculate hash
    if not args.quiet and args.verbose:
        print(f"Calculating {args.algorithm.upper()} hash for {file_path}...")

    try:
        calculated = calculate_hash(file_path, args.algorithm)
    except (PermissionError, OSError) as e:
        print(f"Error reading file: {e}")
        return

    if not args.quiet:
        print(f"Calculated hash: {calculated}")

    # Determine comparison status
    if not args.expected:
        status = "No Expected Hash Provided"
        if not args.quiet:
            print("No expected hash provided for comparison.")
    elif compare_hashes(args.expected, calculated):
        status = "Hashes Match"
        if not args.quiet:
            print("Comparison: Hashes Match")
    else:
        status = "Hashes Mismatch"
        if not args.quiet:
            print("Comparison: Hashes Mismatch")

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build report
    report = build_report(
        file_path.name,
        args.algorithm,
        calculated,
        args.expected or "N/A",
        status,
        generated_at
    )

    if not args.quiet:
        print(report)

    # Export reports
    export_report_txt(report, file_path.name, output_dir)
    export_report_json(
        file_path.name,
        args.algorithm,
        calculated,
        args.expected or "N/A",
        status,
        generated_at,
        output_dir
    )

    if not args.quiet:
        print(f"\nReports saved to: {output_dir}")


if __name__ == "__main__":
    main()