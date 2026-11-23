
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from autoflow.duplicates import (
    find_duplicates,
    calculate_file_hash,
    scan_duplicates,
)

class TestDuplicateFinder(unittest.TestCase):

    def test_scan_duplicates_returns_file_count(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "one.txt").write_text("first")
            (folder / "two.txt").write_text("second")
            (folder / "three.txt").write_text("third")

            duplicates, scanned, skipped = scan_duplicates(str(folder))

            self.assertEqual(scanned, 3)
            self.assertEqual(skipped, 0)
            self.assertEqual(duplicates, {})

    def test_scan_duplicates_counts_duplicate_files(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "one.txt").write_text("same content")
            (folder / "two.txt").write_text("same content")
            (folder / "three.txt").write_text("different content")

            duplicates, scanned, skipped = scan_duplicates(str(folder))

            self.assertEqual(scanned, 3)
            self.assertEqual(skipped, 0)
            self.assertEqual(len(duplicates), 1)
            self.assertEqual(len(list(duplicates.values())[0]), 2)

    def test_scan_duplicates_rejects_missing_folder(self):
        with TemporaryDirectory() as temp:
            missing_folder = Path(temp) / "missing"

            with self.assertRaises(NotADirectoryError):
                scan_duplicates(str(missing_folder))

    def test_finds_identical_files(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)

            first = folder / "photo.jpg"
            second = folder / "photo-copy.jpg"

            first.write_text("same image content")
            second.write_text("same image content")

            duplicates = find_duplicates(str(folder))

            self.assertEqual(len(duplicates), 1)
            duplicate_files = list(duplicates.values())[0]

            self.assertEqual(len(duplicate_files), 2)

    def test_ignores_different_files(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)

            first = folder / "file1.txt"
            second = folder / "file2.txt"

            first.write_text("content one")
            second.write_text("content two")

            duplicates = find_duplicates(str(folder))

            self.assertEqual(len(duplicates), 0)

    def test_returns_empty_when_no_files_exist(self):
        with TemporaryDirectory() as temp:
            duplicates = find_duplicates(temp)

            self.assertEqual(duplicates, {})

    def test_calculates_consistent_hash(self):
        with TemporaryDirectory() as temp:
            file = Path(temp) / "example.txt"
            file.write_text("AutoFlow testing")

            first_hash = calculate_file_hash(file)
            second_hash = calculate_file_hash(file)

            self.assertEqual(first_hash, second_hash)

    def test_skips_unreadable_file_and_continues_scanning(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)

            first = folder / "file1.txt"
            second = folder / "file2.txt"
            unreadable = folder / "unreadable.txt"

            first.write_text("same content")
            second.write_text("same content")
            unreadable.write_text("cannot read this file")

            def simulate_read_error(file_path):
                if file_path.name == "unreadable.txt":
                    raise PermissionError("Permission denied")

                return calculate_file_hash(file_path)

            with patch(
                "autoflow.duplicates.calculate_file_hash",
                side_effect=simulate_read_error
            ):
                duplicates = find_duplicates(str(folder))

            self.assertEqual(len(duplicates), 1)

            duplicate_files = list(duplicates.values())[0]

            self.assertEqual(len(duplicate_files), 2)
            self.assertNotIn(unreadable, duplicate_files)


if __name__ == "__main__":
    unittest.main()
