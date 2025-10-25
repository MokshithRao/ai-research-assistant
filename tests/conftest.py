import os
import sys


def pytest_configure():
    """Ensure the project root is on sys.path so tests can import local packages.

    This helps when running pytest with coverage where the cwd or import paths
    can differ from a straight `python -m pytest` run.
    """
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
