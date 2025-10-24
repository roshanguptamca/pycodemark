# PyCodemark

![PyPI version](https://img.shields.io/pypi/v/pycodemark)
![Python Version](https://img.shields.io/pypi/pyversions/pycodemark)
![License](https://img.shields.io/pypi/l/pycodemark)
![Build](https://github.com/roshanguptamca/pycodemark/actions/workflows/codemark.yml/badge.svg)

---

## Overview

**PyCodemark** is a full-featured Python code review tool that automatically detects style issues, missing docstrings, and other code quality problems.  
It supports **terminal, JSON, and SARIF output** for CI/CD integration and is extensible via plugins.

---

## Features

- Detect missing docstrings, PEP8 violations, and clarity issues
- JSON and SARIF output for CI pipelines
- Plugin system for custom checks
- Pre-commit integration
- Configurable via `pyproject.toml`
- Works with Python 3.13+

---

## Installation

Clone the repository:

```bash
git clone https://github.com/roshanguptamca/pycodemark.git
cd pycodemark
```

Create a Python 3.13 virtual environment:
```bash
python3.13 -m venv venv 
source venv/bin/activate
poetry install
``` 
Quick Start
# Quick Start with PyCodemark

PyCodemark is a **full-featured Python code review tool** that detects style issues, missing docstrings, and other code quality problems. It supports **terminal, JSON, and SARIF output** for CI integration.

## Installation

Install PyCodemark via pip:

```bash
pip install pycodemark
````
Or with Poetry:
```bash
poetry add pycodemark 
````
Run a basic code review:
```bash
codemark review src/
codemark review src/ --format json
codemark review src/ --format sarif    
```

Plugins

Extend PyCodemark by adding custom checks under src/codemark/plugins/.
Each plugin must implement:
```python`
def run(file_path, config):
    """Return a list of issues detected in the file."""
    return []
````
Pre-commit Integration

Add to your .pre-commit-config.yaml:
```yaml repos:
  - repo: local
    hooks:
      - id: codemark
        name: codemark-review
        entry: codemark review --format terminal
        language: system
        types: [python]     
```

Then run:
```bashpre-commit install
```pre-commit install
````
CI/CD Integration (GitHub Actions)

You can integrate PyCodemark in CI pipelines with SARIF reporting.
Example workflow file: .github/workflows/codemark.yml

Runs PyCodemark on every push or pull request

Uploads SARIF results to GitHub for code scanning

Provides automated code quality checks

Configuration

Configure PyCodemark via pyproject.toml:
```toml
[tool.pycodemark]
max_line_length = 88
rules = ["PEP8", "clarity", "docstrings"]
exclude = ["tests/", "migrations/"]
```
Makefile Commands:
- `make lint`: Run code linting
- make venv          # Create virtual environment
- make install       # Install dependencies via Poetry
- make build         # Build package
- make test          # Run tests
- make lint          # Run linter
- make lint-fix      # Automatically fix lint issues
- make review        # Run terminal review
- make review-json   # Run review with JSON output
- make review-sarif  # Run review with SARIF output
- make publish       # Publish to PyPI


Download Documentation:
PDF
HTML

License

MIT License © Roshan Gupta
```yaml

---

If you want, I can also provide a **one-liner command** so you can generate this README automatically on your Mac without manually copying it.  

Do you want me to do that next?

```
