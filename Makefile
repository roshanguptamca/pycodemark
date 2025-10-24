# Makefile for Codemark

# Python and Poetry commands
PYTHON := python3.13
POETRY := poetry

# Default target
.PHONY: help
help:
	@echo "Codemark Makefile Commands:"
	@echo "  make install       - Install dependencies via Poetry"
	@echo "  make venv          - Create virtual environment"
	@echo "  make build         - Build Codemark package"
	@echo "  make test          - Run pytest tests"
	@echo "  make lint          - Run ruff linter"
	@echo "  make review        - Run Codemark review on src/"
	@echo "  make review-json   - Run Codemark review with JSON output"
	@echo "  make review-sarif  - Run Codemark review with SARIF output"
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

# Build package
.PHONY: build
build:
	$(POETRY) build

# Run tests
.PHONY: test
test:
	$(POETRY) run pytest

# Run linter
.PHONY: lint
lint:
	$(POETRY) run ruff src/

# Run Codemark review (terminal output)
.PHONY: review
review:
	$(POETRY) run codemark review src/ --format terminal

# Run Codemark review (JSON output)
.PHONY: review-json
review-json:
	$(POETRY) run codemark review src/ --format json

# Run Codemark review (SARIF output)
.PHONY: review-sarif
review-sarif:
	$(POETRY) run codemark review src/ --format sarif

# Publish package to PyPI
.PHONY: publish
publish:
	$(POETRY) publish --build --username __token__ --password $(PYPI_TOKEN)
