def generate_report(issues):
    """
    Transform analysis results into a structured report.

    Args:
        issues (list[tuple]): List of issues from analyzer.

    Returns:
        list[tuple]: Report tuples as (summary, suggestion).
    """
    report = []
    for file, line, code, message in issues:
        summary = f"{file}:{line} – [{code}] {message}"
        suggestion = ""
        if code == "MissingDocstring":
            suggestion = "Consider adding a concise docstring explaining the function's purpose."
        elif code == "BareTry":
            suggestion = "Avoid bare try blocks; handle specific exceptions or use 'except Exception as e'."
        report.append((summary, suggestion))
    return report
