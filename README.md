# Codemark

Codemark is a **full-featured Python code review tool** that detects style issues, missing docstrings, and other code quality problems. It supports **terminal, JSON, and SARIF output** for CI integration and is extensible via plugins.

## Features

- Detect missing docstrings, PEP8 violations, and clarity issues
- JSON and SARIF output for CI pipelines
- Plugin system for custom checks
- Pre-commit integration
- Configurable via `pyproject.toml`

---

## Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd codemark
```    
2. Create a Python 3.13 virtual environment:
```bash

python3.13 -m venv .venv
source .venv/bin/activate
``` 
Install dependencies with Poetry:
```bash
poetry install
``` 

Usage
Basic code review:
```bash
codemark review src/
```
Output in JSON:
```bash
codemark review src/ --format json
```

Output in SARIF (for CI):
```bash
codemark review src/ --format sarif
```

Plugins

Add custom checks under src/codemark/plugins/. Each plugin must have a run(file_path, config) function returning a list of issues.

Example plugin: plugins/sample_plugin.py


Pre-commit Integration

Add to your .pre-commit-config.yaml:

repos:
  - repo: local
    hooks:
      - id: codemark
        name: codemark-review
        entry: codemark review --format terminal
        language: system
        types: [python]


Install pre-commit hooks:
```bash
pre-commit install
```
CI Integration (GitHub Actions)

See .github/workflows/codemark.yml for a ready-to-use example that runs Codemark on every push or pull request and uploads SARIF results to GitHub.