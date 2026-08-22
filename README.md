# Hash Checker

A lightweight Python tool for calculating and verifying file hashes, and generating structured reports in **TXT** and **JSON** formats.

Built with Python's standard library, with a focus on **reliability, memory efficiency, maintainability, and file integrity verification**.

---

## Features

- Calculate file hashes using MD5, SHA-1, SHA-256, and SHA-512.
- Read files in chunks for memory-efficient processing.
- Compare calculated hashes against an expected value.
- Generate formatted TXT reports.
- Export structured JSON reports.
- Timestamped report filenames.
- Configurable output directory.
- Command-line interface (CLI) powered by `argparse`.
- Quiet and verbose execution modes.
- Continue safely when file or output errors occur.
- Uses only Python's standard library.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ali-ahmed-dev/hash-checker.git
```

### 2. Navigate to the project directory

```bash
cd hash-checker
```

No external Python packages are required.

---

## Usage

The tool accepts a **file path** followed by optional command-line arguments.

### Calculate a file hash

```bash
python hash_checker.py firmware.bin
```

### Verify a hash

```bash
python hash_checker.py firmware.bin --algorithm sha256 --expected e3b0c44298fc1c149afb...
```

### Save reports to a custom directory

```bash
python hash_checker.py firmware.bin --output ./reports
```

---

## Command-Line Options

| Option | Description |
|--------|-------------|
| `file` | Path to the file to hash. |
| `-a`, `--algorithm` | Hashing algorithm: `md5`, `sha1`, `sha256`, or `sha512`. Default: `sha256`. |
| `-e`, `--expected` | Expected hash value to compare against. |
| `-c`, `--chunk-size` | Chunk size in bytes (default: 4096, range: 512-1048576). |
| `-o`, `--output` | Directory where reports will be saved. Default: current directory. |
| `-q`, `--quiet` | Minimize console output. |
| `-v`, `--verbose` | Display detailed processing progress. |
| `-h`, `--help` | Display the help message and exit. |

---

## Examples

### Calculate a hash

```bash
python hash_checker.py firmware.bin
```

### Verify against an expected SHA-256 hash

```bash
python hash_checker.py firmware.bin -a sha256 -e e3b0c44298fc1c149afb...
```

### Use a custom output directory

```bash
python hash_checker.py firmware.bin -o ./reports
```

### Use quiet mode

```bash
python hash_checker.py firmware.bin --quiet
```

### Use verbose mode

```bash
python hash_checker.py firmware.bin --verbose
```

### Display available options

```bash
python hash_checker.py --help
```

---

## How It Works

The tool processes the selected file in binary mode and calculates its hash incrementally.

```text
Input File
     │
     ▼
Validate File
     │
     ▼
Select Algorithm
     │
     ▼
Read File in Chunks
     │
     ▼
Calculate Hash
     │
     ├── No Expected Hash
     │
     └── Expected Hash
              │
              ▼
        Compare Hashes
              │
              ├── Match
              └── Mismatch
              │
              ▼
        Generate Reports
           ├── TXT
           └── JSON
```

---

## Memory Efficiency

Hash Checker processes files in fixed-size chunks instead of loading the entire file into memory.

The current implementation uses a default chunk size of **4096 bytes**.

```text
Large File
    │
    ▼
Read Chunk
    │
    ▼
Update Hash
    │
    ▼
Read Next Chunk
    │
    ▼
Continue Until EOF
```

This allows large files to be processed with memory usage that does not grow with the complete file size.

---

## Hash Verification

When an expected hash is provided, the calculated hash is compared with the expected value.

Possible results are:

```text
No Expected Hash Provided
Hashes Match
Hashes Mismatch
```

Example:

```text
Algorithm   : SHA256
Calculated  : e3b0c44298fc1c149afb...
Expected    : e3b0c44298fc1c149afb...
Status      : Hashes Match
```

---

## Report Output

### TXT Report

Generates a human-readable report containing the file name, algorithm, calculated hash, expected hash, and verification status.

```text
==================================================
                 HASH CHECKER
==================================================
Generated   : 2026-08-16 14:35:12
File Name   : firmware.bin
Algorithm   : SHA256
Status      : Hashes Match
Calculated  : e3b0c44298fc1c149afb...
Expected    : e3b0c44298fc1c149afb...
==================================================
                 END OF REPORT
==================================================
```

### JSON Report

Generates structured analysis data suitable for further processing and future automation.

```json
{
    "generated_at": "2026-08-16 14:35:12",
    "file_name": "firmware.bin",
    "algorithm": "SHA256",
    "calculated_hash": "e3b0c44298fc1c149afb...",
    "expected_hash": "e3b0c44298fc1c149afb...",
    "status": "Hashes Match"
}
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

## Technologies

- **Python 3**
- **argparse** — command-line interface
- **hashlib** — hash calculation
- **pathlib** — file and directory handling
- **json** — structured report generation
- **datetime** — report timestamps

---

## Requirements

- Python 3.x
- No external dependencies
- Uses Python Standard Library only

---

## Current Version

**v1.3.0**

---

## Development History

The project started as a simple file hashing script and gradually evolved into a command-line tool for file hash calculation and verification.

Major improvements include:

- Multiple hashing algorithm support
- Chunk-based file processing
- Expected hash verification
- TXT report generation
- JSON report generation
- Configurable output directory
- Improved error handling
- Command-line interface
- Quiet and verbose execution modes

The project continues to evolve alongside the author's development in **Python, algorithms, web development, Linux, networking, and cybersecurity**.

---

## Future Development

The project will evolve gradually as new requirements, ideas, and skills emerge.

Potential future improvements include:

- Multiple file verification
- Recursive directory scanning
- Batch hash verification
- Colorized terminal output
- CSV report generation
- Additional file integrity capabilities

> These are long-term ideas rather than a fixed roadmap. Features will be added progressively as the project matures.

---

## Security

Hash Checker is designed as a **file integrity verification and security-oriented development project**.

File hashes can be used to verify whether a file's contents match a known expected value.

Always obtain expected hashes from trusted sources and avoid sharing sensitive file information publicly.

MD5 and SHA-1 are included for compatibility and educational purposes. For modern integrity verification, **SHA-256** or stronger algorithms are preferred.

---

## License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

## Author

**Ali Ahmed**

GitHub:  
https://github.com/ali-ahmed-dev