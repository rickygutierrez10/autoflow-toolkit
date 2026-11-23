
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from autoflow.files import organise_files


class TestFileOrganiser(unittest.TestCase):

    def test_dry_run_does_not_move_files(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            file = folder / "invoice.pdf"
            file.write_text("test document")

            results = organise_files(str(folder), dry_run=True)

            self.assertEqual(
                results["invoice.pdf"],
                "Would move to Documents"
            )
            self.assertTrue(file.exists())

    def test_moves_file_to_correct_folder(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            file = folder / "holiday.jpg"
            file.write_text("test image")

            results = organise_files(str(folder), dry_run=False)

            destination = folder / "Images" / "holiday.jpg"

            self.assertTrue(destination.exists())
            self.assertFalse(file.exists())
            self.assertEqual(
                results["holiday.jpg"],
                "Moved to Images"
            )

    def test_does_not_overwrite_existing_file(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)

            source = folder / "invoice.pdf"
            source.write_text("original")

            documents = folder / "Documents"
            documents.mkdir()

            existing = documents / "invoice.pdf"
            existing.write_text("important existing file")

            results = organise_files(str(folder), dry_run=False)

            self.assertEqual(
                results["invoice.pdf"],
                "Skipped: destination already exists"
            )
            self.assertEqual(existing.read_text(), "important existing file")
            self.assertTrue(source.exists())

    def test_unknown_file_goes_to_other(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            file = folder / "example.xyz"
            file.write_text("test")

            results = organise_files(str(folder), dry_run=False)

            self.assertTrue((folder / "Other" / "example.xyz").exists())
            self.assertEqual(results["example.xyz"], "Moved to Other")


if __name__ == "__main__":
    unittest.main()
