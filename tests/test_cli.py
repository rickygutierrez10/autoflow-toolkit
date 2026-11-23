
import csv
import subprocess
import sys
import tempfile
import unittest

from pathlib import Path
from autoflow.cli import format_size


class TestCLI(unittest.TestCase):

    def test_help_command(self):
        result = subprocess.run(
            [sys.executable, "-m", "autoflow.cli", "--help"],
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("organise", result.stdout)
        self.assertIn("duplicates", result.stdout)

    def test_duplicates_command(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            folder = Path(temporary_folder)

            (folder / "file1.txt").write_text("same content")
            (folder / "file2.txt").write_text("same content")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "autoflow.cli",
                    "duplicates",
                    str(folder)
                ],
                capture_output=True,
                text=True
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("Duplicate group", result.stdout)
            self.assertIn("file1.txt", result.stdout)
            self.assertIn("file2.txt", result.stdout)

    def test_duplicates_command_shows_scan_statistics(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)

            (folder / "one.txt").write_text("same content")
            (folder / "two.txt").write_text("same content")
            (folder / "three.txt").write_text("different content")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "autoflow.cli",
                    "duplicates",
                    str(folder),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("Files scanned: 3", result.stdout)
            self.assertIn("Duplicate groups: 1", result.stdout)
            self.assertIn("Files involved: 2", result.stdout)
            self.assertIn("Files skipped: 0", result.stdout)
            self.assertIn(
                "Potential storage savings: 12.00 bytes",
                result.stdout,
            )

    def test_duplicates_export_creates_csv_report(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)

            first_file = folder / "one.txt"
            second_file = folder / "two.txt"
            report = folder / "duplicates.csv"

            first_file.write_text("same content")
            second_file.write_text("same content")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "autoflow.cli",
                    "duplicates",
                    str(folder),
                    "--export",
                    str(report),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertTrue(report.exists())
            self.assertIn("CSV report:", result.stdout)

            with report.open(
                "r",
                newline="",
                encoding="utf-8"
            ) as csv_file:
                rows = list(csv.DictReader(csv_file))

            self.assertEqual(len(rows), 2)

            exported_paths = {
                row["File Path"] for row in rows
            }

            expected_paths = {
                str(first_file.resolve()),
                str(second_file.resolve()),
            }

            self.assertEqual(exported_paths, expected_paths)

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

    def test_duplicates_export_excludes_existing_report_from_scan(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)

            (folder / "one.txt").write_text("same content")
            (folder / "two.txt").write_text("same content")

            report = folder / "duplicates.csv"
            report.write_text("An old report")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "autoflow.cli",
                    "duplicates",
                    str(folder),
                    "--export",
                    str(report),
                ],
                capture_output=True,
                text=True,
            )

            # The scan should complete, but export should refuse
            # to overwrite the existing report.
            self.assertNotEqual(result.returncode, 0)

            # Only the two text files should be counted.
            self.assertIn("Files scanned: 2", result.stdout)

            # Existing report must remain unchanged.
            self.assertEqual(
                report.read_text(),
                "An old report",
            )

            self.assertIn("Report already exists", result.stderr)

    def test_duplicates_export_does_not_overwrite_existing_report(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)

            (folder / "one.txt").write_text("same content")
            (folder / "two.txt").write_text("same content")

            report = folder / "duplicates.csv"
            report.write_text("Existing report")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "autoflow.cli",
                    "duplicates",
                    str(folder),
                    "--export",
                    str(report),
                ],
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(
                report.read_text(),
                "Existing report",
            )
            self.assertIn("Report already exists", result.stderr)

    def test_duplicates_export_creates_report_without_duplicates(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)

            (folder / "unique.txt").write_text("unique content")

            report = folder / "duplicates.csv"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "autoflow.cli",
                    "duplicates",
                    str(folder),
                    "--export",
                    str(report),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertTrue(report.exists())
            self.assertIn("No duplicate files found.", result.stdout)

            with report.open(
                "r",
                newline="",
                encoding="utf-8"
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

    def test_organise_rejects_missing_folder(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            missing_folder = Path(temporary_folder) / "missing"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "autoflow.cli",
                    "organise",
                    str(missing_folder)
                ],
                capture_output=True,
                text=True
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Error:", result.stderr)

    def test_duplicates_rejects_missing_folder(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            missing_folder = Path(temporary_folder) / "missing"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "autoflow.cli",
                    "duplicates",
                    str(missing_folder)
                ],
                capture_output=True,
                text=True
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Error:", result.stderr)

    def test_organise_help_shows_recursive_option(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "autoflow.cli",
                "organise",
                "--help",
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("--recursive", result.stdout)

    def test_recursive_organise_command_previews_subfolders(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            subfolder = folder / "Downloads"
            subfolder.mkdir()

            (subfolder / "photo.jpg").write_text("photo")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "autoflow.cli",
                    "organise",
                    str(folder),
                    "--recursive",
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn(
                "Downloads/photo.jpg: Would move to Images",
                result.stdout,
            )
            self.assertTrue((subfolder / "photo.jpg").exists())

    def test_normal_organise_command_does_not_scan_subfolders(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            subfolder = folder / "Downloads"
            subfolder.mkdir()

            (subfolder / "photo.jpg").write_text("photo")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "autoflow.cli",
                    "organise",
                    str(folder),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("No files found to organise.", result.stdout)
            self.assertTrue((subfolder / "photo.jpg").exists())

    def test_format_size_displays_bytes(self):
        self.assertEqual(format_size(500), "500.00 bytes")

    def test_format_size_converts_to_kilobytes(self):
        self.assertEqual(format_size(1024), "1.00 KB")

    def test_format_size_converts_to_megabytes(self):
        self.assertEqual(format_size(1024 * 1024), "1.00 MB")

    def test_format_size_converts_to_gigabytes(self):
        self.assertEqual(
            format_size(1024 * 1024 * 1024),
            "1.00 GB",
        )


if __name__ == "__main__":
    unittest.main()
