# Hash Checker Roadmap

This document outlines the planned improvements and future roadmap for **Hash Checker**. The current release (**v1.0.0**) supports multiple hashing algorithms, hash verification, TXT and JSON report generation, and includes 16 unit tests with automated testing via GitHub Actions.

The following items are planned for future releases.

---

## 🚨 High Priority

These improvements focus on accuracy, reliability, and maintainability.

* [✓] Improve input validation for user-provided file paths and hash values.
* [✓] Expand exception handling with more specific error messages where appropriate.
* [✓] Make the file chunk size configurable for easier performance tuning.
* [✓] Add timestamp-based report filenames to prevent overwriting previous reports.

---

## 🛠️ Medium Priority

These features will improve flexibility and usability.

* [✓] Add command-line argument support using `argparse`.
* [✓] Add unit tests covering core functionality (16 tests).
* [✓] Add automated testing via GitHub Actions.
* [✓] Add pytest support with conftest.py and pytest.ini.
* [ ] Support batch verification of multiple files.
* [ ] Improve report metadata with additional verification details.
* [ ] Allow users to choose custom output locations for generated reports.

---

## 💡 Low Priority

Quality-of-life improvements planned for future releases.

* [ ] Export reports in CSV format.
* [ ] Add optional colorized terminal output.
* [ ] Improve report formatting and customization.
* [ ] Display hash calculation progress for large files.

---

## 🚀 Long-Term Goals

Larger features planned for future major versions.

* [ ] Verify entire directories recursively.
* [ ] Generate checksum manifest files.
* [ ] Verify files against checksum manifest files.
* [ ] Add a graphical user interface (GUI).

---

## Project Roadmap

| Version                  | Status     |
| ------------------------ | ---------- |
| **Current Release**      | **v1.3.3** |
| **Next Planned Release** | **v1.4.0** |

---

Contributions, suggestions, and feature requests are always welcome as the project continues to evolve.