from pathlib import Path
import hashlib

def calculate_hash(filename):
    hash_obj = hashlib.sha256()
    with open(filename, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def generate_report():
    pass


def main():
    print("Welcome to the Hash Checker Tool")

    try:
        filename = Path(input("Enter the file path: "))
        file_hash = calculate_hash(filename)
        print("SHA-256 Hash:")
        print(file_hash)
    except FileNotFoundError:
        print("Status: File not found.")


if __name__ == "__main__":
    main()
