# Hash Checker

A Python command-line tool that calculates and verifies file hashes using multiple hashing algorithms, then generates detailed verification reports in both TXT and JSON formats.

---

## Features

* Calculate file hashes using:

  * MD5
  * SHA-1
  * SHA-256
  * SHA-512
* Read files in chunks for improved memory efficiency.
* Compare calculated hashes against expected values.
* Generate a formatted verification report.
* Export reports as **TXT** files.
* Export reports as **JSON** files named after the target file.

---

## Built With

* Python 3.x
* `hashlib`
* `pathlib`
* `datetime`
* `json`

---

## Requirements

* Python 3.x
* No external dependencies.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/ali-ahmed-dev/hash-checker.git
```

Navigate to the project directory:

```bash
cd hash-checker
```

---

## Usage

Run the program:

```bash
python hash_checker.py
```

Then:

1. Enter the target file path.
2. Select a hashing algorithm.
3. Enter the expected hash.
4. View the verification result.
5. Find the generated reports (named after your target file) in the project directory.
---

## Example Output

```text
==================================================
                 HASH CHECKER
==================================================
Generated   : 2026-07-29 14:35:12
File Name   : firmware.bin
Algorithm   : SHA256
Status      : Hashes Match
Calculated  : e3b0c44298fc1c149afb...
Expected    : e3b0c44298fc1c149afb...
==================================================
                 END OF REPORT
==================================================
```

---

## Project Structure

```text
hash-checker/
│
├── hash_checker.py
├── README.md
├── LICENSE
└── .gitignore
```

---

## Future Improvements

* Verify multiple files in a single run.
* Support recursive directory scanning.
* Verify hashes from batch hash list files.
* Add colorized terminal output.
* Export reports in CSV format.
* Input validation: automatically trims hash inputs and validates file paths before processing.
* Configurable chunk size for performance tuning.

---

## License

This project is licensed under the MIT License.

---

## Version

**v1.1.0**

---

## Author

**Ali Ahmed**
