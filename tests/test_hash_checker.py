"""
Unit tests for the Hash Checker.
"""

import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import hash_checker


class TestCalculateHash(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_hash_of_known_content_sha256(self):
        file = self.root / "test.txt"
        file.write_text("hello", encoding="utf-8")

        result = hash_checker.calculate_hash(file, "sha256", 4096)

        expected = (
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        )
        self.assertEqual(result, expected)

    def test_hash_of_known_content_md5(self):
        file = self.root / "test.txt"
        file.write_text("hello", encoding="utf-8")

        result = hash_checker.calculate_hash(file, "md5", 4096)

        expected = "5d41402abc4b2a76b9719d911017c592"
        self.assertEqual(result, expected)

    def test_same_content_same_hash(self):
        f1 = self.root / "a.txt"
        f2 = self.root / "b.txt"
        f1.write_text("same content", encoding="utf-8")
        f2.write_text("same content", encoding="utf-8")

        self.assertEqual(
            hash_checker.calculate_hash(f1, "sha256", 4096),
            hash_checker.calculate_hash(f2, "sha256", 4096)
        )

    def test_different_content_different_hash(self):
        f1 = self.root / "a.txt"
        f2 = self.root / "b.txt"
        f1.write_text("content A", encoding="utf-8")
        f2.write_text("content B", encoding="utf-8")

        self.assertNotEqual(
            hash_checker.calculate_hash(f1, "sha256", 4096),
            hash_checker.calculate_hash(f2, "sha256", 4096)
        )

    def test_unsupported_algorithm_raises_value_error(self):
        file = self.root / "test.txt"
        file.write_text("hello", encoding="utf-8")

        with self.assertRaises(ValueError):
            hash_checker.calculate_hash(file, "invalid_algo", 4096)

    def test_hash_with_small_chunk_size(self):
        file = self.root / "test.txt"
        file.write_text("hello world", encoding="utf-8")

        result_large = hash_checker.calculate_hash(file, "sha256", 4096)
        result_small = hash_checker.calculate_hash(file, "sha256", 1)

        self.assertEqual(result_large, result_small)


class TestCompareHashes(unittest.TestCase):

    def test_identical_hashes_match(self):
        h = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        self.assertTrue(hash_checker.compare_hashes(h, h))

    def test_case_insensitive(self):
        h_lower = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        h_upper = h_lower.upper()
        self.assertTrue(hash_checker.compare_hashes(h_upper, h_lower))

    def test_whitespace_trimmed(self):
        h = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        self.assertTrue(hash_checker.compare_hashes(f"  {h}\n", h))

    def test_different_hashes_do_not_match(self):
        h1 = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        h2 = "5d41402abc4b2a76b9719d911017c592"
        self.assertFalse(hash_checker.compare_hashes(h1, h2))


class TestBuildReport(unittest.TestCase):

    def test_report_contains_all_fields(self):
        report = hash_checker.build_report(
            "test.bin",
            "sha256",
            "abc123",
            "abc123",
            "Hashes Match",
            "2026-09-17 12:00:00"
        )

        self.assertIn("HASH CHECKER", report)
        self.assertIn("test.bin", report)
        self.assertIn("SHA256", report)
        self.assertIn("Hashes Match", report)
        self.assertIn("abc123", report)
        self.assertIn("2026-09-17 12:00:00", report)
        self.assertIn("END OF REPORT", report)


class TestExportFunctions(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("builtins.print")
    def test_export_txt_creates_file(self, mock_print):
        report = "Test report content"

        hash_checker.export_report_txt(
            report, "test.bin", self.root
        )

        files = list(self.root.glob("*.txt"))
        self.assertEqual(len(files), 1)

    @patch("builtins.print")
    def test_export_txt_content(self, mock_print):
        report = "Test report content"

        hash_checker.export_report_txt(
            report, "test.bin", self.root
        )

        files = list(self.root.glob("*.txt"))
        self.assertEqual(
            files[0].read_text(encoding="utf-8"),
            report,
        )

    @patch("builtins.print")
    def test_export_json_creates_file(self, mock_print):
        hash_checker.export_report_json(
            "test.bin",
            "sha256",
            "abc123",
            "abc123",
            "Hashes Match",
            "2026-09-17 12:00:00",
            self.root,
        )

        files = list(self.root.glob("*.json"))
        self.assertEqual(len(files), 1)

    @patch("builtins.print")
    def test_export_json_content(self, mock_print):
        hash_checker.export_report_json(
            "test.bin",
            "sha256",
            "abc123",
            "abc123",
            "Hashes Match",
            "2026-09-17 12:00:00",
            self.root,
        )

        files = list(self.root.glob("*.json"))
        loaded = json.loads(files[0].read_text(encoding="utf-8"))
        self.assertEqual(loaded["file_name"], "test.bin")
        self.assertEqual(loaded["algorithm"], "SHA256")
        self.assertEqual(loaded["status"], "Hashes Match")

    @patch("builtins.print")
    def test_export_json_default_output_dir(self, mock_print):
        with patch("hash_checker.Path.cwd", return_value=self.root):
            hash_checker.export_report_json(
                "test.bin",
                "sha256",
                "abc",
                "abc",
                "Hashes Match",
                "2026-09-17 12:00:00",
            )

        files = list(self.root.glob("*.json"))
        self.assertEqual(len(files), 1)


if __name__ == "__main__":
    unittest.main()