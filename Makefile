# Makefile for PyCodemark

# Python and Poetry commands
PYTHON := python3.13
POETRY := poetry
SRC := src

# Default target
.PHONY: help
help:
	@echo "PyCodemark Makefile Commands:"
	@echo "  make install       - Install dependencies via Poetry"
	@echo "  make venv          - Create virtual environment"
	@echo "  make build         - Build PyCodemark package"
	@echo "  make test          - Run pytest tests"
	@echo "  make lint          - Run ruff linter"
	@echo "  make lint-fix      - Automatically fix lint issues"
	@echo "  make review        - Run PyCodemark review on src/"
	@echo "  make review-json   - Run PyCodemark review with JSON output"
	@echo "  make review-sarif  - Run PyCodemark review with SARIF output"
	@echo "  make smart-review  - Run AI-powered review"
	@echo "  make version       - Generate dynamic version (Git or timestamp)"
	@echo "  make publish       - Build and publish package to PyPI"
	@echo "  make docs          - Generate PDF and HTML docs from README"

# Create virtual environment
.PHONY: venv
venv:
	$(PYTHON) -m venv .venv
	@echo "Virtual environment created in .venv/"

# Install dependencies
.PHONY: install
install:
	$(POETRY) install

# Generate dynamic version
.PHONY: version
version:
	@echo "Generating dynamic version..."
	@if git describe --tags --abbrev=0 >/dev/null 2>&1; then \
		VERSION=$$(git describe --tags --abbrev=0); \
	else \
		VERSION=0.2.$$(date +%Y%m%d%H%M); \
	fi; \
	echo "__version__ = '$$VERSION'" > $(SRC)/codemark/version.py; \
	echo "Version generated: $$VERSION"

# Build package
.PHONY: build
build: version
	$(POETRY) build

# Run tests
.PHONY: test
test:
	$(POETRY) run pytest

# Run linter
.PHONY: lint
lint:
	$(POETRY) run ruff $(SRC)/ tests/

# Automatically fix lint issues
# Lint and auto-fix with Ruff + format with Black
.PHONY: lint-fix
lint-fix:
	@echo "Running ruff auto-fix..."
	$(POETRY) run ruff src/ tests/ --fix
	@echo "Formatting code with Black..."
	$(POETRY) run black src/ tests/ --line-length 120

# Run static code review (terminal)
.PHONY: review
review:
	$(POETRY) run pycodemark review $(SRC)/ --format terminal

# Run static code review (JSON)
.PHONY: review-json
review-json:
	$(POETRY) run pycodemark review $(SRC)/ --format json

# Run static code review (SARIF)
.PHONY: review-sarif
review-sarif:
	$(POETRY) run pycodemark review $(SRC)/ --format sarif

# Run AI-powered review (terminal)
.PHONY: smart-review
smart-review:
	$(POETRY) run pycodemark smart-review $(SRC)/ --format terminal

# Publish package to PyPI
.PHONY: publish
publish: build
	@echo "Publishing PyCodemark to PyPI..."
	$(POETRY) publish --username __token__ --password $$PYPI_TOKEN

# Generate documentation (PDF & HTML)
.PHONY: docs
docs:
	pandoc README.md -o pycodemark-docs.pdf --metadata title="PyCodemark Documentation"
	pandoc README.md -s -o pycodemark-docs.html

# Format code with Black
.PHONY: format
format:
	@echo "Formatting code with Black..."
	$(POETRY) run black src/ tests/ --line-length 120