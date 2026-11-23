
from pathlib import Path
import subprocess
import sys
import tempfile

from autoflow.files import organise_files


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
            (demo_folder / filename).write_text(
                content,
                encoding="utf-8",
            )

        print("\nAUTOFLOW TOOLKIT DEMONSTRATION")
        print("=" * 45)

        # Demonstrate file organisation.
        print("\n1. FILE ORGANISATION PREVIEW")
        print("-" * 45)

        results = organise_files(
            str(demo_folder),
            dry_run=True,
        )

        for filename, result in results.items():
            print(f"{filename}: {result}")

        print("\nNo files were moved. This was a preview only.")

        # Demonstrate duplicate detection and CSV export.
        print("\n2. DUPLICATE DETECTION AND CSV EXPORT")
        print("-" * 45)

        report_path = demo_folder / "duplicate-report.csv"

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "autoflow.cli",
                "duplicates",
                str(demo_folder),
                "--export",
                str(report_path),
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print("The demonstration encountered an error.")
            print(result.stderr)
            return

        print(result.stdout)

        # Display the generated CSV report.
        print("\n3. GENERATED CSV REPORT")
        print("-" * 45)

        if report_path.exists():
            print(report_path.read_text(encoding="utf-8"))
        else:
            print("CSV report could not be found.")

        print("\nDemonstration complete!")
        print("All sample files were stored in a temporary folder.")
        print("The temporary folder will now be cleaned up.")


if __name__ == "__main__":
    main()
