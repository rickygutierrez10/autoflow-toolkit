import logging
import argparse
logging.basicConfig(
    filename="autoflow.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("autoflow")
from pathlib import Path

from autoflow.files import organise_files



def main():
    parser = argparse.ArgumentParser(
        prog="autoflow",
        description="A simple file automation toolkit."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

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

    args = parser.parse_args()

    if args.command == "organise":
        try:
            results = organise_files(args.folder, dry_run=not args.apply)

            logger.info("AutoFlow organised folder: %s", args.folder)

            if not results:
                print("No files found to organise.")
                return

            print("\nAUTOFLOW RESULTS")
            print("-" * 35)

            for filename, result in results.items():
                print(f"{filename}: {result}")
                logger.info("%s: %s", filename, result)

        except (NotADirectoryError, PermissionError) as error:
            parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()

