
import hashlib
import logging
from pathlib import Path

logger = logging.getLogger("autoflow")


def calculate_file_hash(file_path: Path) -> str:
    """Calculate the SHA-256 hash of a file."""

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def scan_duplicates(folder: str) -> tuple[dict, int, int]:
    """Find duplicate files using file sizes before calculating hashes."""

    source = Path(folder).expanduser().resolve()

    if not source.is_dir():
        raise NotADirectoryError(f"Folder does not exist: {source}")

    files_by_size = {}
    scanned_files = 0
    skipped_files = 0

    # First, group files by size.
    for file_path in source.rglob("*"):
        if not file_path.is_file():
            continue

        try:
            file_size = file_path.stat().st_size

            files_by_size.setdefault(file_size, []).append(file_path)
            scanned_files += 1

        except OSError as error:
            skipped_files += 1

            logger.warning(
                "Could not inspect file %s: %s",
                file_path,
                error
            )

    # Only hash files that share a size.
    hashes = {}

    for file_size, paths in files_by_size.items():
        if len(paths) < 2:
            continue

        for file_path in paths:
            try:
                file_hash = calculate_file_hash(file_path)

                hashes.setdefault(file_hash, []).append(file_path)

            except OSError as error:
                skipped_files += 1

                logger.warning(
                    "Could not read file %s: %s",
                    file_path,
                    error
                )

    duplicates = {
        file_hash: paths
        for file_hash, paths in hashes.items()
        if len(paths) > 1
    }

    return duplicates, scanned_files, skipped_files


def calculate_duplicate_savings(duplicates: dict) -> int:
    """Calculate potential storage savings from duplicate files."""

    potential_savings = 0

    for paths in duplicates.values():
        if len(paths) < 2:
            continue

        try:
            file_size = paths[0].stat().st_size

            potential_savings += file_size * (len(paths) - 1)

        except OSError as error:
            logger.warning(
                "Could not calculate duplicate file size for %s: %s",
                paths[0],
                error
            )

    return potential_savings


def find_duplicates(folder: str) -> dict:
    """Find files with identical contents inside a folder."""

    duplicates, _, _ = scan_duplicates(folder)

    return duplicates
