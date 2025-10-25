"""Module description."""

import os
import subprocess
from .logger import logger


def get_python_files(path: str) -> list[str]:
    """Return all Python files in a directory or a single file."""
    files = []
    if os.path.isdir(path):
        for root, _, filenames in os.walk(path):
            for f in filenames:
                if f.endswith(".py"):
                    files.append(os.path.join(root, f))
    elif path.endswith(".py"):
        files.append(path)
    return files


def read_file(file_path: str) -> str:
    """Read a Python file and return its content."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error("Failed to read file %s: %s", file_path, e)
        return ""


def analyze_file(path: str, config: dict) -> list[dict]:
    """Perform static analysis using simple rules"""
    issues = []
    max_len = config.get("max_line_length", 88)
    ignore = config.get("ignore_rules", [])

    files = get_python_files(path)
    for file_path in files:
        content = read_file(file_path)
        lines = content.splitlines()
        for i, line in enumerate(lines, start=1):
            if "LineLength" not in ignore and len(line.rstrip("\n")) > max_len:
                issues.append(
                    {
                        "file": file_path,
                        "line": i,
                        "code": "LineLength",
                        "message": f"Line too long ({len(line.rstrip())} > {max_len})",
                    }
                )
            if "MissingDocstring" not in ignore and i == 1 and not line.strip().startswith('"""'):
                issues.append(
                    {
                        "file": file_path,
                        "line": i,
                        "code": "MissingDocstring",
                        "message": "Missing file docstring",
                    }
                )
    return issues


def auto_fix_file(file_path: str, line_length: int = 88) -> bool:
    """Automatically fix code using black"""
    try:
        subprocess.run(
            ["black", "--line-length", str(line_length), file_path],
            check=True,
            capture_output=True,
        )
        logger.info("Auto-fixed %s", file_path)
        return True
    except subprocess.CalledProcessError as e:
        logger.error("Failed to auto-fix %s: %s", file_path, e.stderr.decode())
        return False
