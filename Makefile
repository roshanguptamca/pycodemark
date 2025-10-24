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
	@echo "  make review        - Run PyCodemark review on src/"
	@echo "  make review-json   - Run PyCodemark review with JSON output"
	@echo "  make review-sarif  - Run PyCodemark review with SARIF output"
	@echo "  make version       - Generate dynamic version (Git or timestamp)"
	@echo "  make publish       - Build and publish package to PyPI"

# Create virtual environment
.PHONY: venv
venv:
	$(PYTHON) -m venv .venv
	@echo "Virtual environment created in .venv/"

# Install dependencies
.PHONY: install
install:
	$(POETRY) install

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
	$(POETRY) run ruff $(SRC)/

.PHONY: lint-fix
lint-fix:
	$(POETRY) run ruff src/ --fix

# Run PyCodemark review (terminal output)
.PHONY: review
review:
	$(POETRY) run pycodemark review $(SRC)/ --format terminal

# Run PyCodemark review (JSON output)
.PHONY: review-json
review-json:
	$(POETRY) run pycodemark review $(SRC)/ --format json

# Run PyCodemark review (SARIF output)
.PHONY: review-sarif
review-sarif:
	$(POETRY) run pycodemark review $(SRC)/ --format sarif

# Publish package to PyPI
.PHONY: publish
publish: build
	@echo "Publishing PyCodemark to PyPI..."
	$(POETRY) publish --username __token__ --password $$PYPI_TOKEN

# Generate docs
.PHONY: docs
docs:
	pandoc README.md -o pycodemark-docs.pdf --metadata title="PyCodemark Documentation"
	pandoc README.md -s -o pycodemark-docs.html