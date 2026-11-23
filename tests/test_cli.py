
import subprocess
import sys
import tempfile
import unittest

from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
