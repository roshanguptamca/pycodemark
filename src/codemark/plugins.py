import importlib
import pkgutil

def load_plugins():
    """
    Load and return all plugin modules from the codemark/plugins directory.

    Returns:
        generator: Generator yielding plugin run functions.
    """
    for finder, name, ispkg in pkgutil.iter_modules(["codemark/plugins"]):
        module = importlib.import_module(f"codemark.plugins.{name}")
        yield module.run
