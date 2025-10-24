import ast
import os

def analyze_file(path, config):
    """
    Analyze a Python file or directory for code issues.

    Args:
        path (str): Path to a file or directory.
        config (dict): Configuration rules.

    Returns:
        list[tuple]: List of issues as (file_path, line, code, message).
    """
    issues = []

    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(".py"):
                    issues += analyze_file(os.path.join(root, f), config)
        return issues

    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        issues.append((path, e.lineno, "SyntaxError", str(e)))
        return issues

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and not ast.get_docstring(node):
            issues.append(
                (path, node.lineno, "MissingDocstring", f"Function '{node.name}' has no docstring.")
            )
        if isinstance(node, ast.Try) and not node.handlers:
            issues.append((path, node.lineno, "BareTry", "Try block without exception handlers."))

    return issues
