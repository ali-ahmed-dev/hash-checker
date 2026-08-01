from pathlib import Path
import hashlib
import json
from datetime import datetime

SEPARATOR = "=" * 50
SUPPORTED_ALGORITHMS = {
    "1": "md5",
    "2": "sha1",
    "3": "sha256",
    "4": "sha512",
}
REPORT_FILENAME = "hash_checker_report.txt"

HEADER = f"{SEPARATOR}\n                 HASH CHECKER \n{SEPARATOR}"
FOOTER = f"{SEPARATOR}\n                 END OF REPORT\n{SEPARATOR}"


def calculate_hash(file_path, algorithm):
    hash_obj = hashlib.new(algorithm)
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def compare_hashes(expected_hash, calculated_hash):
    return expected_hash.lower() == calculated_hash.lower()


def build_report(file_name, algorithm, calculated_hash, expected_hash, status, generated_at):
    report_lines = [
        HEADER,
        f"Generated   : {generated_at}",
        f"File Name   : {file_name}",
        f"Algorithm   : {algorithm.upper()}",
        f"Calculated  : {calculated_hash}",
        f"Expected    : {expected_hash}",
        f"Status      : {status}",
        FOOTER
    ]
    return "\n".join(report_lines)


def export_report(report_lines):
    with open(REPORT_FILENAME, "w", encoding="utf-8") as file:
        file.write(report_lines)


def export_report_json(file_name, algorithm, calculated_hash, expected_hash, status, generated_at):
    report_dict = {
        "generated": generated_at,
        "file_name": file_name,
        "algorithm": algorithm.upper(),
        "calculated_hash": calculated_hash,
        "expected_hash": expected_hash,
        "status": status
    }
    json_filename = f"{Path(file_name).stem}_report.json"
    with open(json_filename, "w", encoding="utf-8") as file:
        json.dump(report_dict, file, indent=4, ensure_ascii=False)


def main():
    print("Welcome to the Hash Checker Tool")

    try:
        user_input = input("Enter the file path: ").strip()
        if not user_input:
            print("Status: No file path provided.")
            return
        file_path = Path(user_input)
        print("Choose hash algorithm \n1.MD5\n2.SHA1\n3.SHA256\n4.SHA512\n")
        algorithm_num = input("choose an option (1-4):")
        algorithm = SUPPORTED_ALGORITHMS[algorithm_num]
        calculated_hash = calculate_hash(file_path, algorithm)
        expected_hash = input("Enter the hash to compare: ").strip()
        if not expected_hash:
            print("Status: No hash provided for comparison.")
            return
        status = "Hashes Match" if compare_hashes(expected_hash, calculated_hash) else "Hashes Mismatch"
        generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_lines = build_report(file_path.name, algorithm, calculated_hash, expected_hash, status, generated_at)
        print(report_lines)
        export_report(report_lines)
        export_report_json(file_path.name, algorithm, calculated_hash, expected_hash, status, generated_at)
    except KeyError:
        print("Error: Invalid algorithm selection.")
    except FileNotFoundError:
        print("Status: File not found.")
    except IsADirectoryError:
        print("Error: The specified path is a directory.")

    except PermissionError:
        print("Error: Permission denied while accessing the file.")

    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
