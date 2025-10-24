import tomli
from pathlib import Path

def load_config():
    """
    Load Codemark configuration from pyproject.toml.

    Returns:
        dict: Configuration values for rules, line length, etc.
    """
    pyproject = Path("pyproject.toml")
    if pyproject.exists():
        with open(pyproject, "rb") as f:
            data = tomli.load(f)
            return data.get("tool", {}).get("codemark", {})
    return {}
