
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from autoflow.files import organise_files


class TestFileOrganiser(unittest.TestCase):

    def test_dry_run_does_not_move_files(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            file = folder / "document.pdf"
            file.write_text("test document")

            results = organise_files(str(folder), dry_run=True)

            self.assertEqual(
                results["document.pdf"],
                "Would move to Documents/document.pdf"
            )
            self.assertTrue(file.exists())
            self.assertFalse((folder / "Documents").exists())

    def test_moves_files_into_category_folders(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            file = folder / "photo.jpg"
            file.write_text("test image")

            results = organise_files(str(folder), dry_run=False)

            destination = folder / "Images" / "photo.jpg"

            self.assertEqual(
                results["photo.jpg"],
                "Moved to Images/photo.jpg"
            )
            self.assertTrue(destination.exists())
            self.assertFalse(file.exists())

    def test_does_not_overwrite_existing_files(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)

            file = folder / "photo.jpg"
            file.write_text("new image")

            destination_folder = folder / "Images"
            destination_folder.mkdir()

            existing_file = destination_folder / "photo.jpg"
            existing_file.write_text("original image")

            results = organise_files(str(folder), dry_run=False)

            renamed_file = destination_folder / "photo_1.jpg"

            self.assertEqual(
                results["photo.jpg"],
                "Moved to Images/photo_1.jpg"
            )
            self.assertTrue(renamed_file.exists())
            self.assertEqual(renamed_file.read_text(), "new image")
            self.assertEqual(existing_file.read_text(), "original image")
            self.assertFalse(file.exists())

    def test_unknown_file_types_go_into_other_folder(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            file = folder / "example.xyz"
            file.write_text("test")

            results = organise_files(str(folder), dry_run=False)

            destination = folder / "Other" / "example.xyz"

            self.assertTrue(destination.exists())
            self.assertEqual(
                results["example.xyz"],
                "Moved to Other/example.xyz"
            )

    def test_continues_when_file_move_fails(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)

            failing_file = folder / "failed.pdf"
            successful_file = folder / "success.jpg"

            failing_file.write_text("document")
            successful_file.write_text("image")

            real_move = shutil.move

            def simulate_move_error(source, destination):
                if Path(source).name == "failed.pdf":
                    raise PermissionError("Permission denied")

                return real_move(source, destination)

            with patch(
                "autoflow.files.shutil.move",
                side_effect=simulate_move_error
            ):
                results = organise_files(str(folder), dry_run=False)

            self.assertIn("Error:", results["failed.pdf"])
            self.assertTrue(failing_file.exists())

            self.assertEqual(
                results["success.jpg"],
                "Moved to Images/success.jpg"
            )
            self.assertTrue(
                (folder / "Images" / "success.jpg").exists()
            )

    def test_recursive_organises_files_in_subfolders(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            subfolder = folder / "Downloads"
            subfolder.mkdir()

            file = subfolder / "photo.jpg"
            file.write_text("test image")

            results = organise_files(
                str(folder),
                dry_run=False,
                recursive=True,
            )

            destination = folder / "Images" / "photo.jpg"

            self.assertTrue(destination.exists())
            self.assertFalse(file.exists())
            self.assertEqual(
                results["Downloads/photo.jpg"],
                "Moved to Images/photo.jpg",
            )

    def test_recursive_dry_run_does_not_move_files(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            subfolder = folder / "Downloads"
            subfolder.mkdir()

            file = subfolder / "document.pdf"
            file.write_text("test document")

            results = organise_files(
                str(folder),
                dry_run=True,
                recursive=True,
            )

            self.assertTrue(file.exists())
            self.assertEqual(
                results["Downloads/document.pdf"],
                "Would move to Documents/document.pdf",
            )

    def test_recursive_does_not_reorganise_category_folders(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            category = folder / "Images"
            category.mkdir()

            file = category / "photo.jpg"
            file.write_text("test image")

            results = organise_files(
                str(folder),
                dry_run=False,
                recursive=True,
            )

            self.assertTrue(file.exists())
            self.assertEqual(results, {})

    def test_recursive_handles_duplicate_filenames(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)

            first_folder = folder / "Work"
            second_folder = folder / "Personal"

            first_folder.mkdir()
            second_folder.mkdir()

            (first_folder / "report.pdf").write_text("Work report")
            (second_folder / "report.pdf").write_text("Personal report")

            results = organise_files(
                str(folder),
                dry_run=False,
                recursive=True,
            )

            destination = folder / "Documents"

            self.assertTrue((destination / "report.pdf").exists())
            self.assertTrue((destination / "report_1.pdf").exists())

            contents = {
                (destination / "report.pdf").read_text(),
                (destination / "report_1.pdf").read_text(),
            }

            self.assertEqual(
                contents,
                {"Work report", "Personal report"},
            )

            self.assertEqual(len(results), 2)

    def test_recursive_handles_three_duplicate_filenames(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)

            for name in ["Work", "Personal", "Archive"]:
                subfolder = folder / name
                subfolder.mkdir()
                (subfolder / "report.pdf").write_text(name)

            organise_files(
                str(folder),
                dry_run=False,
                recursive=True,
            )

            destination = folder / "Documents"

            self.assertTrue((destination / "report.pdf").exists())
            self.assertTrue((destination / "report_1.pdf").exists())
            self.assertTrue((destination / "report_2.pdf").exists())

    def test_recursive_duplicate_dry_run_shows_unique_names(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)

            first_folder = folder / "Work"
            second_folder = folder / "Personal"

            first_folder.mkdir()
            second_folder.mkdir()

            first_file = first_folder / "report.pdf"
            second_file = second_folder / "report.pdf"

            first_file.write_text("Work report")
            second_file.write_text("Personal report")

            results = organise_files(
                str(folder),
                dry_run=True,
                recursive=True,
            )

            self.assertEqual(
                len(results),
                2,
            )

            self.assertEqual(
                set(results.values()),
                {
                    "Would move to Documents/report.pdf",
                    "Would move to Documents/report_1.pdf",
                },
            )

            self.assertTrue(first_file.exists())
            self.assertTrue(second_file.exists())


if __name__ == "__main__":
    unittest.main()
