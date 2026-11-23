
from pathlib import Path
import logging
import shutil

logger = logging.getLogger("autoflow")

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Archives": [".zip", ".rar", ".7z"],
    "Spreadsheets": [".xlsx", ".xls", ".csv"],
}


def get_unique_destination(
    destination: Path,
    reserved: set = None,
) -> Path:
    """Return a filename that does not already exist or is reserved."""

    if reserved is None:
        reserved = set()

    if not destination.exists() and destination not in reserved:
        return destination

    counter = 1

    while True:
        unique_name = (
            f"{destination.stem}_{counter}{destination.suffix}"
        )
        unique_destination = destination.with_name(unique_name)

        if (
            not unique_destination.exists()
            and unique_destination not in reserved
        ):
            return unique_destination

        counter += 1


def organise_files(
    folder: str,
    dry_run: bool = True,
    recursive: bool = False,
) -> dict:
    """Organise files into folders based on their extensions."""

    source = Path(folder).expanduser().resolve()

    if not source.is_dir():
        raise NotADirectoryError(f"Folder does not exist: {source}")

    results = {}
    planned_destinations = set()

    category_names = set(FILE_CATEGORIES) | {"Other"}

    if recursive:
        files = source.rglob("*")
    else:
        files = source.iterdir()

    for file in files:
        try:
            if not file.is_file():
                continue

            relative_path = file.relative_to(source)

            # Skip files already inside top-level category folders.
            if relative_path.parts[0] in category_names:
                continue

            category = next(
                (
                    name
                    for name, extensions in FILE_CATEGORIES.items()
                    if file.suffix.lower() in extensions
                ),
                "Other",
            )

            destination_folder = source / category
            destination = destination_folder / file.name

            if file == destination:
                continue

            # Reserve each planned destination to prevent preview conflicts.
            destination = get_unique_destination(
                destination,
                planned_destinations,
            )

            planned_destinations.add(destination)

            relative_destination = destination.relative_to(source)

            if dry_run:
                results[str(relative_path)] = (
                    f"Would move to {relative_destination}"
                )
                continue

            destination.parent.mkdir(parents=True, exist_ok=True)

            shutil.move(str(file), str(destination))

            results[str(relative_path)] = (
                f"Moved to {relative_destination}"
            )

        except OSError as error:
            logger.warning(
                "Could not organise file %s: %s",
                file,
                error,
            )

            results[str(file.relative_to(source))] = f"Error: {error}"

    return results
