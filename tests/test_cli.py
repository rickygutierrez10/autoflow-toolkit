
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


if __name__ == "__main__":
    unittest.main()
