# AutoFlow Toolkit

A simple Python automation toolkit that helps organise files and detect duplicate files using their contents.

## Features

- Automatically organises files into categories.
- Supports images, documents, videos, archives and spreadsheets.
- Preview changes before moving anything.
- Safe mode by default.
- Prevents existing files from being overwritten.
- Detects duplicate files using SHA-256 hashing.
- Logs organisation activity.
- Includes automated tests.

## Installation

Clone the repository:

```bash
git clone https://github.com/rickygutierrez10/autoflow-toolkit.git
cd autoflow-toolkit
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install AutoFlow:

```bash
python -m pip install -e .
```

## Usage

### 1. Organise files

Preview file organisation without moving anything:

```bash
autoflow organise /path/to/your/folder
```

Actually move the files:

```bash
autoflow organise /path/to/your/folder --apply
```

### 2. Find duplicate files

Scan a folder for files with identical contents:

```bash
autoflow duplicates /path/to/your/folder
```

AutoFlow uses SHA-256 hashing to compare file contents. Files with identical contents are displayed together in duplicate groups.

## Supported File Categories

| Category | Extensions |
|---|---|
| Images | jpg, jpeg, png, gif, webp |
| Documents | pdf, docx, doc, txt |
| Videos | mp4, mov, avi |
| Archives | zip, rar, 7z |
| Spreadsheets | xlsx, xls, csv |

Unrecognised file types are placed in an `Other` folder.
## Running the Demonstration

AutoFlow includes a demonstration script that shows how to preview file organisation and detect duplicate files using sample data.

Run the demonstration from the project root:

```bash
python examples/demo.py
```

The script creates temporary sample files, demonstrates both features, and automatically cleans up the temporary folder when finished.

## Running Tests

Run the automated test suite:

```bash
python -m unittest discover -s tests -v
```

## Project Status

AutoFlow is an early-stage open-source project. Contributions, suggestions and improvements are welcome.

## License

This project is licensed under the MIT License.