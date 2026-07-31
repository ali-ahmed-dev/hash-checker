
def calculate_hash(filename):
    pass


def generate_report():
    pass


def main():
    print("Welcome to the Hash Checker Tool")

    try:
        filename = (input("Enter the file name: "))
        calculate_hash(filename)
    except FileNotFoundError:
        print("Status: File not found.")


if __name__ == "__main__":
    main()
