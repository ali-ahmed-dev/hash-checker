"""
Hash Checker - A tool for calculating and verifying file hashes.
"""

from __future__ import annotations
from datetime import datetime
from pathlib import Path
import argparse
import hashlib
import json


# ===================== CONSTANTS =====================
CHUNK_MIN = 512
CHUNK_MAX = 1_048_576  # 1 MiB

SEPARATOR = "=" * 50

HEADER = f"{SEPARATOR}\n                 HASH CHECKER \n{SEPARATOR}"
FOOTER = f"{SEPARATOR}\n                 END OF REPORT\n{SEPARATOR}"

SUPPORTED_ALGORITHMS = ["md5", "sha1", "sha256", "sha512"]
DEFAULT_CHUNK_SIZE = 4096


# ===================== CORE FUNCTIONS =====================
def calculate_hash(
    file_path: Path,
    algorithm: str,
    chunk_size: int
) -> str:
    """
    Calculate the hash of a file using the specified algorithm.

    Args:
        file_path (Path): Path to the file.
        algorithm (str): Hashing algorithm.
        chunk_size (int): Buffer size for reading the file.

    Returns:
        str: Hexadecimal hash digest.

    Raises:
        ValueError: If the algorithm is not supported.
        OSError: If the file cannot be read.
    """

    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hashing algorithm: {algorithm}")

    hash_obj = hashlib.new(algorithm)

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(chunk_size), b""):
            hash_obj.update(chunk)

    return hash_obj.hexdigest()


def compare_hashes(expected: str, calculated: str) -> bool:
    """
    Compare expected hash with calculated hash.

    Comparison is case-insensitive and ignores surrounding whitespace.
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
    Build a formatted hash verification report.
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


def export_report_txt(
    report: str,
    file_name: str,
    output_dir: Path,
    quiet: bool = False
) -> None:
    """Export the report to a timestamped TXT file."""

    timestamp = get_timestamp()
    txt_filename = f"{Path(file_name).stem}_report_{timestamp}.txt"
    report_path = output_dir / txt_filename

    report_path.write_text(report, encoding="utf-8")

    if not quiet:
        print(f"Report exported to {report_path}")


def export_report_json(
    file_name: str,
    algorithm: str,
    calculated: str,
    expected: str,
    status: str,
    generated_at: str,
    output_dir: Path | None = None,
    quiet: bool = False
) -> None:
    """Export report data to a timestamped JSON file."""

    if output_dir is None:
        output_dir = Path.cwd()

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
            json.dumps(
                report_data,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        if not quiet:
            print(f"Report exported to {report_path}")

    except (PermissionError, OSError) as e:
        print(
            f"Error: Could not write JSON report "
            f"to {report_path}. {e}"
        )


# ===================== ARGUMENT PARSER =====================
def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the CLI argument parser.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Calculate and verify file hashes "
            "using multiple algorithms."
        ),
        epilog="""
Examples:
  %(prog)s firmware.bin -a sha256
  %(prog)s firmware.bin -a sha256 -e HASH_VALUE
  %(prog)s firmware.bin -a md5 -o ./reports
  %(prog)s firmware.bin -c 65536 -v
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "file",
        help="Path to the file to hash"
    )

    parser.add_argument(
        "-a",
        "--algorithm",
        choices=SUPPORTED_ALGORITHMS,
        default="sha256",
        help=(
            "Hashing algorithm to use. "
            f"Choices: {', '.join(SUPPORTED_ALGORITHMS)} "
            "(default: sha256)"
        )
    )

    parser.add_argument(
        "-e",
        "--expected",
        help="Expected hash value to compare against"
    )

    parser.add_argument(
        "-c",
        "--chunk-size",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        help=(
            f"Chunk size in bytes "
            f"(default: {DEFAULT_CHUNK_SIZE}, "
            f"range: {CHUNK_MIN}-{CHUNK_MAX})"
        )
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Directory to save reports (default: current directory)"
    )

    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress normal output"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print detailed processing information"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="Hash Checker v1.3.3"
    )

    return parser


# ===================== MAIN =====================
def main() -> int:
    """
    Main entry point for the Hash Checker CLI.
    """

    parser = create_parser()
    args = parser.parse_args()

    # ---------- Validate file ----------
    file_path = Path(args.file)

    if not file_path.exists():
        print(f"Error: File '{args.file}' not found.")
        return 1

    if not file_path.is_file():
        print(f"Error: '{args.file}' is a directory, not a file.")
        return 1

    # ---------- Validate chunk size ----------
    if not CHUNK_MIN <= args.chunk_size <= CHUNK_MAX:
        print(
            f"Error: chunk size must be between "
            f"{CHUNK_MIN} and {CHUNK_MAX} bytes."
        )
        return 1

    # ---------- Determine output directory ----------
    output_dir = (
        Path(args.output)
        if args.output
        else Path.cwd()
    )

    try:
        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )
    except (PermissionError, OSError) as e:
        print(
            f"Error: Could not create output directory "
            f"'{output_dir}'. {e}"
        )
        return 1

    # ---------- Calculate hash ----------
    if args.verbose and not args.quiet:
        print(
            f"Calculating {args.algorithm.upper()} "
            f"hash for {file_path}..."
        )

    try:
        calculated = calculate_hash(
            file_path,
            args.algorithm,
            args.chunk_size
        )

    except (PermissionError, OSError) as e:
        print(f"Error reading file: {e}")
        return 1

    except ValueError as e:
        print(f"Error: {e}")
        return 1

    # ---------- Display calculated hash ----------
    if not args.quiet:
        print(f"Calculated hash: {calculated}")

    # ---------- Verify hash ----------
    if args.expected is None:
        status = "No Expected Hash Provided"
        expected = "N/A"

        if not args.quiet:
            print("No expected hash provided for comparison.")

    elif compare_hashes(args.expected, calculated):
        status = "Hashes Match"
        expected = args.expected

        if not args.quiet:
            print("Comparison: Hashes Match")

    else:
        status = "Hashes Mismatch"
        expected = args.expected

        if not args.quiet:
            print("Comparison: Hashes Mismatch")

    # ---------- Generate timestamp ----------
    generated_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # ---------- Build report ----------
    report = build_report(
        file_path.name,
        args.algorithm,
        calculated,
        expected,
        status,
        generated_at
    )

    if not args.quiet:
        print(report)

    # ---------- Export reports ----------
    try:
        export_report_txt(
            report,
            file_path.name,
            output_dir,
            quiet=args.quiet
        )

        export_report_json(
            file_path.name,
            args.algorithm,
            calculated,
            expected,
            status,
            generated_at,
            output_dir,
            quiet=args.quiet
        )

    except (PermissionError, OSError) as e:
        print(f"Error exporting report: {e}")
        return 1

    if not args.quiet:
        print(f"\nReports saved to: {output_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())