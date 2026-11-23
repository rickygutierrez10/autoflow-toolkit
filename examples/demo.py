
from pathlib import Path
import tempfile

from autoflow.files import organise_files
from autoflow.duplicates import find_duplicates


def main():
    # Create a temporary folder for our demonstration.
    with tempfile.TemporaryDirectory() as temporary_folder:
        demo_folder = Path(temporary_folder)

        # Create sample files.
        (demo_folder / "photo.jpg").write_text("Sample photo")
        (demo_folder / "document.txt").write_text("Sample document")
        (demo_folder / "photo-copy.jpg").write_text("Sample photo")

        print("\nAUTOFLOW DEMONSTRATION")
        print("-" * 35)

        # Preview file organisation.
        print("\n1. Previewing file organisation:")

        results = organise_files(str(demo_folder), dry_run=True)

        for filename, result in results.items():
            print(f"{filename}: {result}")

        # Find duplicate files.
        print("\n2. Finding duplicate files:")

        duplicates = find_duplicates(str(demo_folder))

        if duplicates:
            for paths in duplicates.values():
                print("\nDuplicate group:")

                for path in paths:
                    print(f"  {path}")
        else:
            print("No duplicate files found.")

        print("\nDemonstration complete!")


if __name__ == "__main__":
    main()
