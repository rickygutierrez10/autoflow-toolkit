
import argparse
import csv
import logging
from pathlib import Path

from autoflow.duplicates import (
    scan_duplicates,
    calculate_duplicate_savings,
)
from autoflow.files import organise_files


LOG_FILE = Path("autoflow.log")

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("autoflow")


def format_size(size: int) -> str:
    """Convert bytes into a human-readable storage size."""

    units = ["bytes", "KB", "MB", "GB", "TB"]
    size = float(size)

    for unit in units:
        if size < 1024 or unit == "TB":
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} TB"


def export_duplicates(duplicates: dict, output_file: str) -> Path:
    """Export duplicate file details to a CSV report."""

    destination = Path(output_file).expanduser().resolve()

    if destination.exists():
        raise FileExistsError(
            f"Report already exists: {destination}"
        )

    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            "Duplicate Group",
            "File Path",
            "File Size (Bytes)",
            "Potential Storage Savings (Bytes)",
        ])

        for file_hash, paths in duplicates.items():
            try:
                file_size = paths[0].stat().st_size
            except OSError:
                file_size = ""

            potential_savings = (
                file_size * (len(paths) - 1)
                if isinstance(file_size, int)
                else ""
            )

            for path in paths:
                try:
                    current_size = path.stat().st_size
                except OSError:
                    current_size = ""

                writer.writerow([
                    file_hash,
                    str(path),
                    current_size,
                    potential_savings,
                ])

    logger.info("Duplicate report exported: %s", destination)

    return destination


def main():
    parser = argparse.ArgumentParser(
        prog="autoflow",
        description="A simple file automation toolkit."
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # Organise command
    organise_parser = subparsers.add_parser(
        "organise",
        help="Organise files into folders."
    )

    organise_parser.add_argument(
        "folder",
        help="Folder containing files to organise."
    )

    organise_parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually move files. Without this option, only preview changes."
    )

    organise_parser.add_argument(
        "--recursive",
        action="store_true",
        help="Also organise files inside subfolders."
    )

    # Duplicate detection command
    duplicate_parser = subparsers.add_parser(
        "duplicates",
        help="Find duplicate files."
    )

    duplicate_parser.add_argument(
        "folder",
        help="Folder to scan for duplicate files."
    )

    duplicate_parser.add_argument(
        "--export",
        metavar="CSV_FILE",
        help="Export duplicate results to a CSV file."
    )

    args = parser.parse_args()

    if args.command == "organise":
        try:
            results = organise_files(
                args.folder,
                dry_run=not args.apply,
                recursive=args.recursive
            )

            logger.info(
                "AutoFlow organised folder: %s (recursive: %s)",
                args.folder,
                args.recursive
            )

            if not results:
                print("No files found to organise.")
                logger.info("No files found to organise.")
                return

            print("\nAUTOFLOW RESULTS")
            print("-" * 35)

            for filename, result in results.items():
                print(f"{filename}: {result}")
                logger.info("%s: %s", filename, result)

            print(f"\nFiles processed: {len(results)}")
            print(f"Activity log: {LOG_FILE.resolve()}")

        except (NotADirectoryError, PermissionError) as error:
            logger.error("Organisation failed: %s", error)
            parser.exit(1, f"Error: {error}\n")

    elif args.command == "duplicates":
        try:
            logger.info("Starting duplicate scan: %s", args.folder)

            duplicates, scanned_files, skipped_files = scan_duplicates(
                args.folder
            )

            total_duplicate_files = sum(
                len(paths) for paths in duplicates.values()
            )

            storage_savings = calculate_duplicate_savings(duplicates)

            if not duplicates:
                print("No duplicate files found.")
            else:
                print("\nAUTOFLOW DUPLICATES")
                print("-" * 35)

                for file_hash, paths in duplicates.items():
                    print("\nDuplicate group:")
                    logger.info("Duplicate group found: %s", file_hash)

                    for path in paths:
                        print(f"  {path}")
                        logger.info("Duplicate file: %s", path)

            print("\nSCAN SUMMARY")
            print("-" * 35)
            print(f"Files scanned: {scanned_files}")
            print(f"Duplicate groups: {len(duplicates)}")
            print(f"Files involved: {total_duplicate_files}")
            print(f"Files skipped: {skipped_files}")
            print(
                "Potential storage savings: "
                f"{format_size(storage_savings)}"
            )

            if args.export:
                report_path = export_duplicates(
                    duplicates,
                    args.export
                )
                print(f"CSV report: {report_path}")

            print(f"Activity log: {LOG_FILE.resolve()}")

            logger.info(
                "Duplicate scan completed. Scanned: %s, groups: %s, "
                "duplicate files: %s, skipped: %s, potential savings: %s",
                scanned_files,
                len(duplicates),
                total_duplicate_files,
                skipped_files,
                storage_savings
            )

        except (
            NotADirectoryError,
            PermissionError,
            FileExistsError,
            OSError,
        ) as error:
            logger.error("Duplicate scan or export failed: %s", error)
            parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
