from pathlib import Path
import hashlib

SUPPORTED_ALGORITHMS = {
    "1": "md5",
    "2": "sha1",
    "3": "sha256",
    "4": "sha512",
}


def calculate_hash(filename, algorithm):
    hash_obj = hashlib.new(algorithm)
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
        print("Choose hash algorithm \n1.MD5\n2.SHA1\n3.SHA256\n4.SHA512):")
        algorithm_num = input("choose an option (1-4):")
        algorithm = SUPPORTED_ALGORITHMS[algorithm_num]
        file_hash = calculate_hash(filename, algorithm)
        print(" Hash:", file_hash)
    except KeyError:
        print("Error: Invalid algorithm selection")
    except FileNotFoundError:
        print("Status: File not found.")


if __name__ == "__main__":
    main()
