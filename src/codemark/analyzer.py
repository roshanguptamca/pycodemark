import ast
import os
from .plugins import load_plugins


def analyze_file(path, config):
    """
    Analyze a Python file or directory for code issues.

    Args:
        path (str): Path to a file or directory.
        config (dict): Configuration rules.

    Returns:
        list[dict]: List of issues as dictionaries with file_path, line, code, and message.
    """
    issues = []

    # Recursively analyze directories
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(".py"):
                    issues += analyze_file(os.path.join(root, f), config)
        return issues

    # Read file content
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    # Parse AST
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        issues.append({"file": path, "line": e.lineno, "code": "SyntaxError", "message": str(e)})
        return issues

    # Basic AST checks
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and not ast.get_docstring(node):
            issues.append(
                {
                    "file": path,
                    "line": node.lineno,
                    "code": "MissingDocstring",
                    "message": f"Function '{node.name}' has no docstring.",
                }
            )
        if isinstance(node, ast.Try) and not node.handlers:
            issues.append(
                {
                    "file": path,
                    "line": node.lineno,
                    "code": "BareTry",
                    "message": "Try block without exception handlers.",
                }
            )

    # Plugin-based checks
    plugins = load_plugins()
    for plugin in plugins:
        try:
            plugin_issues = plugin.run(path, config)
            for issue in plugin_issues:
                issues.append(
                    {
                        "file": path,
                        "line": issue.get("line"),
                        "code": issue.get("code"),
                        "message": issue.get("message"),
                    }
                )
        except Exception as e:
            issues.append(
                {"file": path, "line": 0, "code": "PluginError", "message": f"Plugin {plugin.__name__} failed: {e}"}
            )

    return issues
