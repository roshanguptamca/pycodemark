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
Environment Variables

PyCodemark requires an OpenAI API key to perform AI-powered smart code reviews. You can also optionally specify which OpenAI model to use.

1. OpenAI API Key

Set your API key as an environment variable:
```bash
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxx" 
```
This is required for the smart-review command.

The tool will use this key to authenticate with the OpenAI API.

You can obtain your key from OpenAI API Keys
2. 2. Optional: Specify AI Model

By default, PyCodemark uses the gpt-5 model for smart reviews. 
You can override it with the environment variable CODEMARK_MODEL:

```bash
export CODEMARK_MODEL="gpt-5" 
```

If not set, gpt-5 will be used automatically.
You can specify any OpenAI chat-capable model available to your account.
Example models: gpt-5, gpt-5.1, gpt-4, gpt-4-32k.

Quick Example:
```bash
export OPENAI_API_KEY="sk-xxxx"
export CODEMARK_MODEL="gpt-5"

# Run AI-powered review
codemark smart-review src/

```
Any issues detected by the AI will appear in the terminal table, JSON, or SARIF output depending on the chosen --format.

If your quota is exceeded or the API fails, the tool will log the error in the report.

4. Security Tips
Do not commit your API key to version control.
Store keys securely in environment variables or secret managers.
You can also use .env files with tools like direnv or python-dotenv.

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
