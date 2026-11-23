
from pathlib import Path
import tempfile

from autoflow.files import organise_files
from autoflow.duplicates import scan_duplicates


def main():
    with tempfile.TemporaryDirectory() as temporary_folder:
        demo_folder = Path(temporary_folder)

        # Create realistic sample files.
        sample_files = {
            "photo.jpg": "Sample image content",
            "document.txt": "Sample document content",
            "invoice.pdf": "Sample invoice content",
            "invoice-copy.pdf": "Sample invoice content",
            "data.csv": "Name,Age\nJohn,25",
        }

        for filename, content in sample_files.items():
            (demo_folder / filename).write_text(content)

        print("\nAUTOFLOW TOOLKIT DEMONSTRATION")
        print("=" * 40)

        # Demonstrate file organisation.
        print("\n1. FILE ORGANISATION PREVIEW")
        print("-" * 40)

        results = organise_files(str(demo_folder), dry_run=True)

        for filename, result in results.items():
            print(f"{filename}: {result}")

        # Demonstrate duplicate detection.
        print("\n2. DUPLICATE FILE DETECTION")
        print("-" * 40)

        duplicates, scanned, skipped = scan_duplicates(
            str(demo_folder)
        )

        if duplicates:
            for paths in duplicates.values():
                print("\nDuplicate group:")

                for path in paths:
                    print(f"  {path.name}")
        else:
            print("No duplicate files found.")

        # Display scan statistics.
        total_duplicate_files = sum(
            len(paths) for paths in duplicates.values()
        )

        print("\nSCAN SUMMARY")
        print("-" * 40)
        print(f"Files scanned: {scanned}")
        print(f"Duplicate groups: {len(duplicates)}")
        print(f"Files involved: {total_duplicate_files}")
        print(f"Files skipped: {skipped}")

        print("\nDemonstration complete!")


if __name__ == "__main__":
    main()
