"""Module description."""

import subprocess
from pathlib import Path
from .logger import logger
from .analyzer import analyze_file, get_python_files

AUTO_FIXABLE = {"LineLength", "MissingDocstring"}


def auto_fix(path: str, config: dict) -> list[dict]:
    """
    Automatically fix fixable issues and optionally insert template docstrings.

    Returns:
        List[dict]: Remaining non-fixable issues.
    """
    remaining_issues = []
    files = get_python_files(path)
    max_len = config.get("max_line_length", 88)
    insert_docstrings = config.get("insert_docstrings", True)  # default True

    for file_path in files:
        issues = analyze_file(file_path, config)
        non_fixable = []

        for issue in issues:
            code = issue.get("code")
            if code == "LineLength":
                try:
                    subprocess.run(
                        ["black", "--line-length", str(max_len), file_path],
                        check=True,
                        capture_output=True,
                    )
                    issue["auto_fixed"] = True
                    logger.info("Auto-fixed %s in %s", code, file_path)
                except subprocess.CalledProcessError as e:
                    logger.error(
                        "Failed to auto-fix %s in %s: %s",
                        code,
                        file_path,
                        e.stderr.decode(),
                    )
                    non_fixable.append(issue)

            elif code == "MissingDocstring" and insert_docstrings:
                if _insert_template_docstring(file_path):
                    issue["auto_fixed"] = True
                    logger.info("Inserted template docstring in %s", file_path)
                else:
                    non_fixable.append(issue)
            else:
                non_fixable.append(issue)

        remaining_issues.extend(non_fixable)

    return remaining_issues


def _insert_template_docstring(file_path: str) -> bool:
    """
    Inserts a basic template docstring at the top of the Python file.
    Returns True if inserted, False if already present.
    """
    try:
        content = Path(file_path).read_text(encoding="utf-8")
        if not content.startswith('"""'):
            docstring = '"""Module description."""\n\n'
            Path(file_path).write_text(docstring + content, encoding="utf-8")
            return True
        return False
    except Exception as e:
        logger.error("Failed to insert docstring in %s: %s", file_path, e)
        return False
