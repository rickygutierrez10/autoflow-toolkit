
# AutoFlow Toolkit

A simple Python automation toolkit that helps organise files into folders based on their file extensions.

## Features

- Automatically organises files into categories.
- Supports images, documents, videos, archives and spreadsheets.
- Preview changes before moving files.
- Safe mode by default.
- Prevents existing files from being overwritten.
- Logs organisation activity.
- Includes automated tests.

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
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

Preview file organisation without moving anything:

```bash
autoflow organise /path/to/your/folder
```

Actually move the files:

```bash
autoflow organise /path/to/your/folder --apply
```

## Supported File Categories

| Category | Extensions |
|---|---|
| Images | jpg, jpeg, png, gif, webp |
| Documents | pdf, docx, doc, txt |
| Videos | mp4, mov, avi |
| Archives | zip, rar, 7z |
| Spreadsheets | xlsx, xls, csv |

Unrecognised file types are placed in an `Other` folder.

## Running Tests

```bash
python -m unittest discover -s tests -v
```

## Project Status

AutoFlow is an early-stage open-source project. Contributions, suggestions and improvements are welcome.

## License

This project is licensed under the MIT License.
