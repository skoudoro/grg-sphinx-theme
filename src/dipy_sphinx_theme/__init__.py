"""
DIPY Sphinx Theme
"""
from pathlib import Path

__version__ = "1.0.1"
"""dipy-sphinx-theme version"""

def get_html_theme_path():
    """Return list of HTML theme paths."""
    parent = Path(__file__).parent.resolve()
    theme_path = parent / "theme" / "dipy_sphinx_theme"
    return theme_path

def setup(app):
    app.add_html_theme('dipy_sphinx_theme', get_html_theme_path())