# AutoFlow Toolkit

**A Python command-line toolkit for file organisation, duplicate detection and storage analysis.**

AutoFlow Toolkit helps users organise cluttered directories, identify duplicate files and understand how much storage space could potentially be recovered.

It provides safe previews, recursive scanning, duplicate detection, CSV report exports and detailed scan statistics through a simple command-line interface.

## Features

- **File Organisation:** Automatically sorts files into folders based on their extensions.
- **Recursive Organisation:** Organises files inside subdirectories when requested.
- **Safe Preview:** Preview proposed file movements before applying changes.
- **Duplicate Detection:** Identifies files with identical contents using SHA-256 hashing.
- **Storage Analysis:** Calculates potential storage savings from duplicate files.
- **Optimised Scanning:** Checks file sizes before hashing to avoid unnecessary processing.
- **CSV Reports:** Export duplicate detection results to a CSV file for further analysis.
- **Report Protection:** Prevents existing CSV reports from being overwritten and excludes the selected report from the duplicate scan.
- **Collision Protection:** Prevents existing files from being overwritten when organising files.
- **Error Handling:** Handles inaccessible files and continues scanning where possible.
- **Activity Logging:** Records important operations and errors.

## Requirements

- Python 3.9 or newer
- pip

## Installation

### Option 1: Install from GitHub

Clone the repository:

```bash
git clone https://github.com/rickygutierrez10/autoflow-toolkit.git
```

Enter the project directory:

```bash
cd autoflow-toolkit
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

Install AutoFlow:

```bash
python -m pip install -e .
```

Verify the installation:

```bash
autoflow --help
```

### Option 2: Build and install locally

Install the build tool:

```bash
python -m pip install build
```

Build the distributions:

```bash
python -m build
```

Install the generated wheel:

```bash
python -m pip install dist/autoflow_toolkit-0.1.0-py3-none-any.whl
```

## Usage

### 1. Organise Files

Preview file organisation:

```bash
autoflow organise /path/to/folder
```

Apply file organisation:

```bash
autoflow organise /path/to/folder --apply
```

Organise files inside subdirectories:

```bash
autoflow organise /path/to/folder --recursive
```

Apply recursive organisation:

```bash
autoflow organise /path/to/folder --recursive --apply
```

**Important:** Without `--apply`, AutoFlow runs in preview mode and does not move files.

### 2. Find Duplicate Files

Scan a directory:

```bash
autoflow duplicates /path/to/folder
```

AutoFlow identifies files with identical contents and displays:

- Files scanned
- Duplicate groups found
- Files involved
- Files skipped
- Potential storage savings

Duplicate detection uses SHA-256 hashing. File sizes are checked first to reduce unnecessary hashing.

**Note:** AutoFlow identifies duplicates and calculates potential savings. It does not automatically delete files.

### 3. Export Duplicate Results to CSV

Export duplicate detection results to a CSV report:

```bash
autoflow duplicates /path/to/folder --export duplicates.csv
```

You can also specify a full output path:

```bash
autoflow duplicates /path/to/folder --export /path/to/reports/duplicates.csv
```

The CSV report includes:

- Duplicate group hash
- File path
- File size in bytes
- Potential storage savings in bytes

AutoFlow creates the report directory if it does not already exist.

**Report protection:** AutoFlow will not overwrite an existing report. If the requested report file already exists, the export is refused and the existing file is left unchanged. When the report is inside the directory being scanned, it is excluded from the duplicate scan.

### 4. Run the Demonstration

Run the included demonstration:

```bash
python examples/demo.py
```

The demonstration creates sample files in a temporary directory and showcases three stages:

1. **File Organisation Preview:** Shows where different files would be organised without moving them.
2. **Duplicate Detection:** Identifies identical files and displays scan statistics, including potential storage savings.
3. **CSV Report Generation:** Creates and displays a CSV report containing the detected duplicate files.

The demonstration uses temporary sample files. It does not reorganise or delete files from your personal directories. The temporary demonstration folder is automatically cleaned up when it finishes.

## Supported File Categories

| Category | Supported extensions |
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

AutoFlow includes automated tests covering:

- File organisation
- Recursive organisation
- Duplicate detection
- File hashing
- Storage savings calculations
- Duplicate scanning optimisation
- CSV report export and protection
- Command-line functionality
- Error handling

## Project Structure

```text
autoflow-toolkit/
├── .github/
│   └── workflows/
│       └── tests.yml
├── autoflow/
│   ├── __init__.py
│   ├── files.py
│   ├── duplicates.py
│   └── cli.py
├── tests/
│   ├── test_files.py
│   ├── test_duplicates.py
│   └── test_cli.py
├── examples/
│   └── demo.py
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
├── run_test.py
└── .gitignore
```

## Contributing

Contributions, suggestions and bug reports are welcome.

If you would like to contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Run the automated test suite.
5. Submit a pull request.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting changes.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Project Status

AutoFlow Toolkit is an actively developed open-source project. New features, improvements and contributions are welcome.

**GitHub Repository:** https://github.com/rickygutierrez10/autoflow-toolkit