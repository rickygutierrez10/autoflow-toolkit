
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from autoflow.duplicates import (
    calculate_duplicate_savings,
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


    def test_calculates_duplicate_storage_savings(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)

            first = folder / "first.txt"
            second = folder / "second.txt"
            third = folder / "third.txt"

            first.write_text("same content")
            second.write_text("same content")
            third.write_text("same content")

            duplicates = {
                "test_hash": [first, second, third]
            }

            savings = calculate_duplicate_savings(duplicates)

            self.assertEqual(
                savings,
                first.stat().st_size * 2,
            )

    def test_returns_zero_when_no_duplicates_exist(self):
        savings = calculate_duplicate_savings({})

        self.assertEqual(savings, 0)

    def test_does_not_count_unique_files_as_savings(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)

            file = folder / "single.txt"
            file.write_text("only one copy")

            duplicates = {
                "test_hash": [file]
            }

            savings = calculate_duplicate_savings(duplicates)

            self.assertEqual(savings, 0)

    def test_does_not_hash_files_with_unique_sizes(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)

            (folder / "small.txt").write_text("abc")
            (folder / "large.txt").write_text("this is longer")

            with patch(
                "autoflow.duplicates.calculate_file_hash"
            ) as hash_mock:
                duplicates, scanned, skipped = scan_duplicates(
                    str(folder)
                )

            self.assertEqual(duplicates, {})
            self.assertEqual(scanned, 2)
            self.assertEqual(skipped, 0)
            hash_mock.assert_not_called()

    def test_hashes_files_with_matching_sizes(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)

            (folder / "first.txt").write_text("hello")
            (folder / "second.txt").write_text("world")

            with patch(
                "autoflow.duplicates.calculate_file_hash",
                wraps=calculate_file_hash,
            ) as hash_mock:
                duplicates, scanned, skipped = scan_duplicates(
                    str(folder)
                )

            self.assertEqual(duplicates, {})
            self.assertEqual(scanned, 2)
            self.assertEqual(skipped, 0)
            self.assertEqual(hash_mock.call_count, 2)

if __name__ == "__main__":
    unittest.main()
