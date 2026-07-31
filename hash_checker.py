from pathlib import Path


def calculate_hash(filename):
    with open(filename, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            pass


def generate_report():
    pass


def main():
    print("Welcome to the Hash Checker Tool")

    try:
        filename = Path(input("Enter the file path: "))
        calculate_hash(filename)
    except FileNotFoundError:
        print("Status: File not found.")


if __name__ == "__main__":
    main()
