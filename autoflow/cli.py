
import logging
import argparse
from pathlib import Path

from autoflow.duplicates import scan_duplicates
from autoflow.files import organise_files


LOG_FILE = Path("autoflow.log")

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("autoflow")


def main():
    parser = argparse.ArgumentParser(
        prog="autoflow",
        description="A simple file automation toolkit."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

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

    # Duplicate detection command
    duplicate_parser = subparsers.add_parser(
        "duplicates",
        help="Find duplicate files."
    )

    duplicate_parser.add_argument(
        "folder",
        help="Folder to scan for duplicate files."
    )

    args = parser.parse_args()

    if args.command == "organise":
        try:
            results = organise_files(args.folder, dry_run=not args.apply)

            logger.info("AutoFlow organised folder: %s", args.folder)

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
            print(f"Activity log: {LOG_FILE.resolve()}")

            logger.info(
                "Duplicate scan completed. Scanned: %s, groups: %s, "
                "duplicate files: %s, skipped: %s",
                scanned_files,
                len(duplicates),
                total_duplicate_files,
                skipped_files
            )

        except (NotADirectoryError, PermissionError) as error:
            logger.error("Duplicate scan failed: %s", error)
            parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
