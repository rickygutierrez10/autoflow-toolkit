
import hashlib
from pathlib import Path


def calculate_file_hash(file_path: Path) -> str:
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def find_duplicates(folder: str) -> dict:
    """Find files with identical contents inside a folder."""
    source = Path(folder).expanduser().resolve()

    if not source.is_dir():
        raise NotADirectoryError(f"Folder does not exist: {source}")

    hashes = {}

    for file_path in source.rglob("*"):
        if not file_path.is_file():
            continue

        file_hash = calculate_file_hash(file_path)
        hashes.setdefault(file_hash, []).append(file_path)

    return {
        file_hash: paths
        for file_hash, paths in hashes.items()
        if len(paths) > 1
    }
