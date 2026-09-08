# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# OS path commands should be uncommented in conf.py file
# so that html utility could access the right project files to
# generate documentation.
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

project = "aiobastion"
copyright = "2023, Gautier Léveillé"
author = "Gautier Léveillé"
language = "en"
html_title = "aiobastion documentation"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
html_static_path = ["_static"]
html_css_files = ["custom.css"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

add_module_names = False
autodoc_member_order = "bysource"
autodoc_typehints = "description"

html_theme = "furo"
html_theme_options = {
    "source_repository": "https://github.com/gira0/cyberark-async",
    "source_branch": "dev",
    "source_directory": "docs/",
}