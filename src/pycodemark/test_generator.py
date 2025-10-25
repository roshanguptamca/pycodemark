"""Automatic Unit Test Generator for PyCodemark with realistic fixtures and GPT support."""

import ast
from pathlib import Path
from .logger import logger

# AI client (centralized)
try:
    from .ai_client import client

    GPT_AVAILABLE = True
except ImportError:
    client = None
    GPT_AVAILABLE = False


def _attach_parents(node):
    """Recursively attach parent references to AST nodes."""
    for child in ast.iter_child_nodes(node):
        child.parent = node
        _attach_parents(child)


def _extract_functions(file_path: Path):
    """Return list of (function_name, class_name) for non-test functions/methods."""
    try:
        tree = ast.parse(file_path.read_text(encoding="utf-8"))
        _attach_parents(tree)
    except SyntaxError:
        logger.warning("⚠️ Skipping invalid syntax in %s", file_path)
        return []

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            parent = getattr(node, "parent", None)
            class_name = parent.name if isinstance(parent, ast.ClassDef) else None
            if not node.name.startswith("test"):
                functions.append((node.name, class_name))
    return functions


def _compute_import_path(file_path: Path) -> str:
    """Compute a relative module import path for a file to fix imports."""
    parts = list(file_path.with_suffix("").parts)
    if parts[0] == "src":
        parts = parts[1:]
    return ".".join(parts)


def smart_review_for_tests(prompt: str) -> str | None:
    """
    Generate AI-powered test code using centralized client.
    Returns code string or None if generation fails.
    """
    if not GPT_AVAILABLE or not client:
        logger.warning("⚠️ AI client unavailable. Skipping GPT generation.")
        return None

    try:
        response = client.chat.completions.create(
            model="gpt-5", messages=[{"role": "user", "content": prompt}], temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error("❌ GPT generation failed: %s", e)
        return None


def _generate_test_content(file_path: Path, functions: list[tuple[str, str | None]], use_ai: bool = False) -> str:
    """Generate a full pytest-compatible test file with realistic fixtures."""
    import_path = _compute_import_path(file_path)
    lines = [
        f'"""Auto-generated realistic tests for {file_path.name}."""',
        "import pytest",
        "from pathlib import Path",
        "from tempfile import TemporaryDirectory",
        f"from {import_path} import *  # import all functions/classes",
        "",
    ]

    # Temporary file fixture
    lines.append("@pytest.fixture\ndef temp_python_file():")
    lines.append("    with TemporaryDirectory() as tmpdir:")
    lines.append(f"        file_path = Path(tmpdir) / '{file_path.name}'")
    lines.append(f"        file_path.write_text(Path('{file_path}').read_text(), encoding='utf-8')")
    lines.append("        yield file_path\n")

    # Generate tests
    for func_name, class_name in functions:
        if use_ai and GPT_AVAILABLE:
            prompt = f"Generate realistic pytest unit test for {func_name} in {file_path.read_text(encoding='utf-8')}"
            ai_code = smart_review_for_tests(prompt)
            if ai_code:
                lines.append(ai_code)
                continue

        # fallback stub
        target = f"{class_name}.{func_name}" if class_name else func_name
        test_name = f"test_{func_name}"
        lines.append(f"def {test_name}(temp_python_file):")
        lines.append(f'    """Auto-generated test for `{target}`."""')
        lines.append("    # Call the function and check basic behavior")
        if class_name:
            lines.append("    try:")
            lines.append(f"        instance = {class_name}()  # TODO: adjust constructor args")
            lines.append(f"        result = getattr(instance, '{func_name}')()")
            lines.append("    except Exception:")
            lines.append("        result = None  # Skip if instantiation fails")
        else:
            lines.append(f"    # TODO: adjust arguments for {func_name}")
            lines.append(f"    result = {func_name}(str(temp_python_file), {{}})")
        lines.append("    assert result is not None\n")

    return "\n".join(lines)


def _generate_tests_for_file(file_path: Path, output_dir: Path, overwrite: bool, use_ai: bool) -> bool:
    """Generate pytest file for one Python module."""
    functions = _extract_functions(file_path)
    if not functions:
        logger.info("⚪ No testable functions found in %s", file_path)
        return False

    output_file = output_dir / f"test_{file_path.stem}.py"
    if output_file.exists() and not overwrite:
        logger.info("⚪ Skipping existing file: %s (use --overwrite to replace)", output_file)
        return False

    output_dir.mkdir(parents=True, exist_ok=True)
    content = _generate_test_content(file_path, functions, use_ai=use_ai)
    output_file.write_text(content, encoding="utf-8")
    logger.info("✅ Created realistic test: %s", output_file)
    return True


def generate_tests(path: str, *, overwrite: bool = False, output_dir: str = "tests", use_ai: bool = False):
    """
    Generate realistic pytest files for all untested functions and class methods.

    Args:
        path (str): Python file or directory to scan
        overwrite (bool): Overwrite existing test files
        output_dir (str): Directory to save generated tests
        use_ai (bool): Generate realistic tests via GPT
    """
    base_path = Path(path)
    tests_path = Path(output_dir)
    tests_path.mkdir(exist_ok=True)

    generated_files = 0
    covered_modules = 0

    if base_path.is_file() and base_path.suffix == ".py":
        if not base_path.name.startswith("test_"):
            if _generate_tests_for_file(base_path, tests_path, overwrite, use_ai):
                covered_modules += 1
                generated_files += 1
    elif base_path.is_dir():
        for py_file in base_path.rglob("*.py"):
            if "tests" in py_file.parts or py_file.name.startswith("test_"):
                continue
            if _generate_tests_for_file(py_file, tests_path, overwrite, use_ai):
                covered_modules += 1
                generated_files += 1
    else:
        logger.error("❌ Invalid path: %s", path)
        return

    logger.info(
        "✨ Test generation complete. %d file(s) created for %d module(s).",
        generated_files,
        covered_modules,
    )
