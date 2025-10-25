"""Module description."""

# src/pycodemark/config.py
import os
import toml

DEFAULT_CONFIG = {
    "checks": {
        "style": True,
        "clarity": True,
        "docstrings": True,
        "type_hints": True,
        "bugs": True,
        "best_practices": True,
        "ai_review": True,
    },
    "max_line_length": 120,
    "model": "gpt-5",
}


def load_config(path: str = None) -> dict:
    """
    Load user configuration from pycodemark.toml.
    Merge with defaults.
    """
    user_config_path = path or "pycodemark.toml"
    config = DEFAULT_CONFIG.copy()

    if os.path.exists(user_config_path):
        try:
            user_config = toml.load(user_config_path)
            user_checks = user_config.get("pycodemark", {}).get("checks", {})
            config.update(user_config.get("pycodemark", {}))
            config["checks"].update(user_checks)
        except Exception:
            pass

    return config
