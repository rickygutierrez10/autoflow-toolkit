# Contributing to AutoFlow Toolkit

Thank you for your interest in contributing to AutoFlow Toolkit!

Contributions, bug reports, feature suggestions and documentation improvements are welcome. Whether you're fixing a bug, improving existing functionality or suggesting a new feature, your help is appreciated.

## Getting Started

Before contributing, make sure you have:

- Python 3.9 or newer
- Git installed
- A GitHub account

### 1. Fork the Repository

Fork the AutoFlow Toolkit repository on GitHub:

https://github.com/rickygutierrez10/autoflow-toolkit

### 2. Clone Your Fork

Replace `YOUR-USERNAME` with your GitHub username:

```bash
git clone https://github.com/YOUR-USERNAME/autoflow-toolkit.git
```

Enter the project directory:

```bash
cd autoflow-toolkit
```

### 3. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 4. Install the Project

Install AutoFlow in editable mode:

```bash
python -m pip install -e .
```

## Making Changes

Before making changes, create a new branch:

```bash
git checkout -b feature/your-feature-name
```

For bug fixes, you can use:

```bash
git checkout -b fix/description-of-fix
```

When contributing:

- Keep changes focused and easy to review.
- Follow the existing project structure and coding style.
- Use clear and descriptive function and variable names.
- Add or update tests when changing functionality.
- Update documentation when necessary.
- Avoid introducing unnecessary dependencies.

## Running Tests

Run the complete test suite before submitting your changes:

```bash
python -m unittest discover -s tests -v
```

All tests should pass before submitting a pull request.

## Submitting a Pull Request

1. Commit your changes with a clear message.
2. Push your branch to your GitHub fork.
3. Open a pull request against the original AutoFlow Toolkit repository.
4. Explain what you changed and why.
5. Include relevant test results.
6. Link any related issues.

Please keep pull requests focused on one improvement or bug fix wherever possible.

## Reporting Bugs

When reporting a bug, please include:

- A clear description of the issue.
- Steps to reproduce the problem.
- Expected behaviour.
- Actual behaviour.
- Relevant error messages or screenshots.
- Your Python version and operating system.

## Suggesting Features

Feature suggestions are welcome.

Please explain:

- What problem the feature would solve.
- How you imagine it working.
- Why it would be useful to AutoFlow users.

It is helpful to discuss larger changes before submitting a pull request.

## Code Quality

We aim to keep AutoFlow:

- Easy to understand.
- Reliable and well tested.
- Compatible with supported Python versions.
- Safe when working with user files.
- Simple to install and use.

## Thank You

Thank you for helping improve AutoFlow Toolkit. Every meaningful contribution helps make the project better for its users and the open-source community.