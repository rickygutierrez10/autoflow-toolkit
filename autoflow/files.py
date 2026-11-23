
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

            destination = source / category / file.name

            if file == destination:
                continue

            if dry_run:
                results[str(relative_path)] = (
                    f"Would move to {category}"
                )
                continue

            if destination.exists():
                results[str(relative_path)] = (
                    "Skipped: destination already exists"
                )
                continue

            destination.parent.mkdir(parents=True, exist_ok=True)

            shutil.move(str(file), str(destination))

            results[str(relative_path)] = (
                f"Moved to {category}"
            )

        except OSError as error:
            logger.warning(
                "Could not organise file %s: %s",
                file,
                error,
            )

            results[str(file.relative_to(source))] = f"Error: {error}"

    return results
