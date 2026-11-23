
import csv
import io
import sys
import tempfile
import unittest

from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from autoflow.cli import format_size, main


class TestCLI(unittest.TestCase):

    def run_cli(self, *arguments):
        """Run the CLI directly and capture its output."""

        stdout = io.StringIO()
        stderr = io.StringIO()

        arguments = [str(argument) for argument in arguments]

        with patch.object(sys, "argv", ["autoflow"] + arguments):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                try:
                    main()
                    returncode = 0
                except SystemExit as error:
                    returncode = error.code

        return returncode, stdout.getvalue(), stderr.getvalue()

    def test_help_command(self):
        returncode, stdout, _ = self.run_cli("--help")

        self.assertEqual(returncode, 0)
        self.assertIn("organise", stdout)
        self.assertIn("duplicates", stdout)

    def test_organise_help_shows_recursive_option(self):
        returncode, stdout, _ = self.run_cli("organise", "--help")

        self.assertEqual(returncode, 0)
        self.assertIn("--recursive", stdout)

    def test_organise_previews_files(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "photo.jpg").write_text("photo")

            returncode, stdout, _ = self.run_cli(
                "organise", folder
            )

            self.assertEqual(returncode, 0)
            self.assertIn("Would move to Images/photo.jpg", stdout)
            self.assertTrue((folder / "photo.jpg").exists())
            self.assertIn("Files processed: 1", stdout)

    def test_organise_apply_moves_files(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "photo.jpg").write_text("photo")

            returncode, stdout, _ = self.run_cli(
                "organise", folder, "--apply"
            )

            self.assertEqual(returncode, 0)
            self.assertIn("Moved to Images/photo.jpg", stdout)
            self.assertTrue((folder / "Images" / "photo.jpg").exists())
            self.assertFalse((folder / "photo.jpg").exists())

    def test_organise_empty_folder(self):
        with tempfile.TemporaryDirectory() as temp:
            returncode, stdout, _ = self.run_cli("organise", temp)

            self.assertEqual(returncode, 0)
            self.assertIn("No files found to organise.", stdout)

    def test_organise_rejects_missing_folder(self):
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "missing"

            returncode, _, stderr = self.run_cli(
                "organise", missing
            )

            self.assertEqual(returncode, 1)
            self.assertIn("Error:", stderr)

    def test_recursive_organise_previews_subfolders(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            subfolder = folder / "Downloads"
            subfolder.mkdir()

            (subfolder / "photo.jpg").write_text("photo")

            returncode, stdout, _ = self.run_cli(
                "organise", folder, "--recursive"
            )

            self.assertEqual(returncode, 0)
            self.assertIn(
                "Downloads/photo.jpg: Would move to Images/photo.jpg",
                stdout,
            )
            self.assertTrue((subfolder / "photo.jpg").exists())

    def test_normal_organise_does_not_scan_subfolders(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            subfolder = folder / "Downloads"
            subfolder.mkdir()

            (subfolder / "photo.jpg").write_text("photo")

            returncode, stdout, _ = self.run_cli(
                "organise", folder
            )

            self.assertEqual(returncode, 0)
            self.assertIn("No files found to organise.", stdout)
            self.assertTrue((subfolder / "photo.jpg").exists())

    def test_duplicates_command(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)

            (folder / "file1.txt").write_text("same content")
            (folder / "file2.txt").write_text("same content")

            returncode, stdout, _ = self.run_cli(
                "duplicates", folder
            )

            self.assertEqual(returncode, 0)
            self.assertIn("Duplicate group", stdout)
            self.assertIn("file1.txt", stdout)
            self.assertIn("file2.txt", stdout)

    def test_duplicates_command_shows_scan_statistics(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)

            (folder / "one.txt").write_text("same content")
            (folder / "two.txt").write_text("same content")
            (folder / "three.txt").write_text("different content")

            returncode, stdout, _ = self.run_cli(
                "duplicates", folder
            )

            self.assertEqual(returncode, 0)
            self.assertIn("Files scanned: 3", stdout)
            self.assertIn("Duplicate groups: 1", stdout)
            self.assertIn("Files involved: 2", stdout)
            self.assertIn("Files skipped: 0", stdout)
            self.assertIn(
                "Potential storage savings: 12.00 bytes",
                stdout,
            )

    def test_duplicates_command_without_duplicates(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "unique.txt").write_text("unique content")

            returncode, stdout, _ = self.run_cli(
                "duplicates", folder
            )

            self.assertEqual(returncode, 0)
            self.assertIn("No duplicate files found.", stdout)
            self.assertIn("Files scanned: 1", stdout)
            self.assertIn("Duplicate groups: 0", stdout)

    def test_duplicates_rejects_missing_folder(self):
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "missing"

            returncode, _, stderr = self.run_cli(
                "duplicates", missing
            )

            self.assertEqual(returncode, 1)
            self.assertIn("Error:", stderr)

    def test_duplicates_export_creates_csv_report(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)

            first_file = folder / "one.txt"
            second_file = folder / "two.txt"
            report = folder / "duplicates.csv"

            first_file.write_text("same content")
            second_file.write_text("same content")

            returncode, stdout, _ = self.run_cli(
                "duplicates", folder, "--export", report
            )

            self.assertEqual(returncode, 0)
            self.assertTrue(report.exists())
            self.assertIn("CSV report:", stdout)

            with report.open(
                "r", newline="", encoding="utf-8"
            ) as csv_file:
                rows = list(csv.DictReader(csv_file))

            self.assertEqual(len(rows), 2)

            exported_paths = {
                row["File Path"] for row in rows
            }

            self.assertEqual(
                exported_paths,
                {str(first_file.resolve()), str(second_file.resolve())},
            )

            for row in rows:
                self.assertEqual(row["File Size (Bytes)"], "12")
                self.assertEqual(
                    row["Potential Storage Savings (Bytes)"],
                    "12",
                )

            self.assertEqual(
                rows[0]["Duplicate Group"],
                rows[1]["Duplicate Group"],
            )

    def test_duplicates_export_creates_empty_report(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "unique.txt").write_text("unique content")

            report = folder / "duplicates.csv"

            returncode, stdout, _ = self.run_cli(
                "duplicates", folder, "--export", report
            )

            self.assertEqual(returncode, 0)
            self.assertTrue(report.exists())
            self.assertIn("No duplicate files found.", stdout)

            with report.open(
                "r", newline="", encoding="utf-8"
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                rows = list(reader)

            self.assertEqual(rows, [])
            self.assertEqual(
                reader.fieldnames,
                [
                    "Duplicate Group",
                    "File Path",
                    "File Size (Bytes)",
                    "Potential Storage Savings (Bytes)",
                ],
            )

    def test_duplicates_export_does_not_overwrite_existing_report(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)

            (folder / "one.txt").write_text("same content")
            (folder / "two.txt").write_text("same content")

            report = folder / "duplicates.csv"
            report.write_text("Existing report")

            returncode, _, stderr = self.run_cli(
                "duplicates", folder, "--export", report
            )

            self.assertEqual(returncode, 1)
            self.assertEqual(report.read_text(), "Existing report")
            self.assertIn("Report already exists", stderr)

    def test_duplicates_export_excludes_existing_report_from_scan(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)

            (folder / "one.txt").write_text("same content")
            (folder / "two.txt").write_text("same content")

            report = folder / "duplicates.csv"
            report.write_text("An old report")

            returncode, stdout, stderr = self.run_cli(
                "duplicates", folder, "--export", report
            )

            self.assertEqual(returncode, 1)
            self.assertIn("Files scanned: 2", stdout)
            self.assertEqual(report.read_text(), "An old report")
            self.assertIn("Report already exists", stderr)

    def test_format_size(self):
        test_cases = [
            (500, "500.00 bytes"),
            (1024, "1.00 KB"),
            (1024 ** 2, "1.00 MB"),
            (1024 ** 3, "1.00 GB"),
            (1024 ** 4, "1.00 TB"),
        ]

        for size, expected in test_cases:
            with self.subTest(size=size):
                self.assertEqual(format_size(size), expected)


if __name__ == "__main__":
    unittest.main()
