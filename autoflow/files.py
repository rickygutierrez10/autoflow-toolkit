
from pathlib import Path
import shutil

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Archives": [".zip", ".rar", ".7z"],
    "Spreadsheets": [".xlsx", ".xls", ".csv"],
}


def organise_files(folder: str, dry_run: bool = True) -> dict:
    """Organise files into folders based on their extensions."""

    source = Path(folder).expanduser().resolve()

    if not source.is_dir():
        raise NotADirectoryError(f"Folder does not exist: {source}")

    results = {}

    for file in source.iterdir():
        if not file.is_file():
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

        if dry_run:
            results[file.name] = f"Would move to {category}"
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)

        if destination.exists():
            results[file.name] = "Skipped: destination already exists"
            continue

        shutil.move(str(file), str(destination))
        results[file.name] = f"Moved to {category}"

    return results

from pathlib import Path
import shutil

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Archives": [".zip", ".rar", ".7z"],
    "Spreadsheets": [".xlsx", ".xls", ".csv"],
}


def organise_files(folder: str, dry_run: bool = True) -> dict:
    """Organise files into folders based on their extensions."""

    source = Path(folder).expanduser().resolve()

    if not source.is_dir():
        raise NotADirectoryError(f"Folder does not exist: {source}")

    results = {}

    for file in source.iterdir():
        if not file.is_file():
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

        if dry_run:
            results[file.name] = f"Would move to {category}"
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)

        if destination.exists():
            results[file.name] = "Skipped: destination already exists"
            continue

        shutil.move(str(file), str(destination))
        results[file.name] = f"Moved to {category}"

    return results
