def run(file_path, config):
    """
    Sample plugin that reports functions with more than 50 lines.

    Args:
        file_path (str): Path to the Python file.
        config (dict): Codemark configuration.

    Returns:
        list[tuple]: List of issues as (file_path, line_number, code, message)
    """
    issues = []
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    lines = code.splitlines()
    if len(lines) > 50:
        issues.append((file_path, 1, "LongFile", "File has more than 50 lines."))
    return issues
