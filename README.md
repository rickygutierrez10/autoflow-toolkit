
# AutoFlow Toolkit

A simple Python toolkit for automating file organisation and detecting duplicate files.

AutoFlow helps users organise cluttered folders, identify duplicate files, and understand what happens during each scan.

## Features

- **File Organisation:** Organises files into folders based on their extensions.
- **Duplicate Detection:** Finds files with identical contents using SHA-256 hashing.
- **Safe Preview:** Preview file organisation before moving anything.
- **Scan Statistics:** Displays files scanned, duplicate groups, files involved, and skipped files.
- **Error Handling:** Skips unreadable files and logs warnings.
- **Activity Logging:** Records important operations and errors.

## Installation

Clone the repository:

```bash
git clone https://github.com/rickygutierrez10/autoflow-toolkit.git
```

Enter the project folder:

```bash
cd autoflow-toolkit
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install AutoFlow:

```bash
python -m pip install -e .
```

## Usage

### 1. Organise Files

Preview file organisation:

```bash
autoflow organise /path/to/folder
```

Actually move files:

```bash
autoflow organise /path/to/folder --apply
```

Without `--apply`, AutoFlow only previews the changes.

### 2. Find Duplicate Files

Scan a folder for duplicates:

```bash
autoflow duplicates /path/to/folder
```

AutoFlow identifies files with identical contents and displays a scan summary.

### 3. Run the Demonstration

```bash
python examples/demo.py
```

The demonstration shows file organisation and duplicate detection using temporary sample files.

## Supported File Categories

| Category | Extensions |
|---|---|
| Images | jpg, jpeg, png, gif, webp |
| Documents | pdf, docx, doc, txt |
| Videos | mp4, mov, avi |
| Archives | zip, rar, 7z |
| Spreadsheets | xlsx, xls, csv |
| Other | All other extensions |

## Running Tests

Run the complete test suite:

```bash
python -m unittest discover -s tests -v
```

## Project Structure

```text
autoflow-toolkit/
├── autoflow/
│   ├── files.py
│   ├── duplicates.py
│   └── cli.py
├── tests/
├── examples/
│   └── demo.py
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── pyproject.toml
```

## Contributing

Contributions, suggestions, and bug reports are welcome.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting changes.

## License

This project is licensed under the MIT License.
