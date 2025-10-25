"""Module description."""

import subprocess
from pathlib import Path
from .logger import logger
from .analyzer import analyze_file, get_python_files

AUTO_FIXABLE = {"LineLength", "MissingDocstring"}


def auto_fix(path: str, config: dict) -> list[dict[str, str | bool]]:
    """
    Automatically fix fixable issues and optionally insert template docstrings.

    Args:
        path (str): Path to Python file or directory.
        config (dict): Configuration dictionary.

    Returns:
        List[dict]: Remaining non-fixable issues, each optionally annotated with 'auto_fixed'.
    """
    remaining_issues: list[dict[str, str | bool]] = []
    files = get_python_files(path)
    max_len = config.get("max_line_length", 88)
    insert_docstrings = config.get("insert_docstrings", True)  # default True

    for file_path in files:
        file_path_obj = Path(file_path)
        issues = analyze_file(str(file_path_obj), config)
        non_fixable = []

        for issue in issues:
            code = issue.get("code")
            issue["auto_fixed"] = False  # default

            if code == "LineLength":
                try:
                    subprocess.run(
                        ["black", "--line-length", str(max_len), str(file_path_obj)],
                        check=True,
                        capture_output=True,
                    )
                    issue["auto_fixed"] = True
                    logger.info("Auto-fixed %s in %s", code, file_path_obj)
                except subprocess.CalledProcessError as e:
                    logger.error(
                        "Failed to auto-fix %s in %s: %s",
                        code,
                        file_path_obj,
                        e.stderr.decode(),
                        exc_info=True,
                    )
                    non_fixable.append(issue)

            elif code == "MissingDocstring" and insert_docstrings:
                if _insert_template_docstring(file_path_obj):
                    issue["auto_fixed"] = True
                    logger.info("Inserted template docstring in %s", file_path_obj)
                else:
                    non_fixable.append(issue)
            else:
                non_fixable.append(issue)

        remaining_issues.extend(non_fixable)

    return remaining_issues


def _insert_template_docstring(file_path: Path | str) -> bool:
    """
    Inserts a basic template docstring at the top of the Python file.

    Args:
        file_path (Path | str): Python file path.

    Returns:
        bool: True if a docstring was inserted, False if already present.
    """
    file_path_obj = Path(file_path)
    try:
        content = file_path_obj.read_text(encoding="utf-8")
        if not content.startswith('"""'):
            docstring = '"""Module description."""\n\n'
            file_path_obj.write_text(docstring + content, encoding="utf-8")
            return True
        return False
    except Exception as e:
        logger.error("Failed to insert docstring in %s: %s", file_path_obj, e, exc_info=True)
        return False
