# src/codemark/reporter.py


def generate_report(issues):
    """
    Transform analysis results into a structured report compatible with renderer.

    Args:
        issues (list[dict or tuple]): List of issues from analyzer or AI.

    Returns:
        list[dict]: Each dict contains 'file', 'line', 'code', 'message'
    """
    report = []

    for issue in issues:
        if isinstance(issue, dict):
            # Already a dict, ensure required keys exist
            report.append(
                {
                    "file": issue.get("file", "unknown"),
                    "line": issue.get("line", 0),
                    "code": issue.get("code", "Unknown"),
                    "message": issue.get("message", ""),
                }
            )
        elif isinstance(issue, (list, tuple)) and len(issue) == 2:
            # Tuple format: (summary, suggestion)
            summary, suggestion = issue
            # Attempt to extract file, line, code from summary if possible
            file_line, code = summary.split(" – ") if " – " in summary else ("unknown", "Unknown")
            if ":" in file_line:
                file, line_str = file_line.split(":", 1)
                try:
                    line = int(line_str)
                except ValueError:
                    line = 0
            else:
                file = file_line
                line = 0

            report.append({"file": file, "line": line, "code": code.strip(), "message": suggestion})
        else:
            # Fallback for unexpected formats
            report.append({"file": "unknown", "line": 0, "code": "Unknown", "message": str(issue)})

    return report
