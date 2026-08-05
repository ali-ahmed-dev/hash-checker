from datetime import datetime
from pathlib import Path
import hashlib
import json


SEPARATOR = "=" * 50
HEADER = f"{SEPARATOR}\n                 HASH CHECKER \n{SEPARATOR}"
FOOTER = f"{SEPARATOR}\n                 END OF REPORT\n{SEPARATOR}"

SUPPORTED_ALGORITHMS = {
    "1": "md5",
    "2": "sha1",
    "3": "sha256",
    "4": "sha512",
}


def calculate_hash(file_path, algorithm):
    hash_obj = hashlib.new(algorithm)
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def compare_hashes(expected, calculated):
    return expected.strip().lower() == calculated.lower()


def build_report(file_name, algorithm, calculated, expected, status, generated_at):
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


def export_report_txt(report, file_name):
    txt_filename = f"{Path(file_name).stem}_report.txt"
    with open(txt_filename, "w", encoding="utf-8") as file:
        file.write(report)


def export_report_json(file_name, algorithm, calculated, expected, status, generated_at):
    report_dict = {
        "generated_at": generated_at,
        "file_name": file_name,
        "algorithm": algorithm.upper(),
        "calculated_hash": calculated,
        "expected_hash": expected,
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
        if not file_path.exists():
            print(f"Error: file '{file_path}' not found.")
            return

        if not file_path.is_file():
            print(f"Error: '{file_path}' is a directory, not a file.")
            return

        print("Choose hash algorithm \n1.MD5\n2.SHA1\n3.SHA256\n4.SHA512\n")
        algorithm_num = input("choose an option (1-4):").strip()
        if algorithm_num not in SUPPORTED_ALGORITHMS:
            print("Error: Invalid algorithm selection.")
            return
        algorithm = SUPPORTED_ALGORITHMS[algorithm_num]
        calculated = calculate_hash(file_path, algorithm)
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
    except KeyError:
        print("Error: Invalid algorithm selection.")

    except PermissionError:
        print("Error: Permission denied while accessing the file.")

    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
