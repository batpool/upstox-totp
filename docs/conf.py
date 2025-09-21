"""
Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path.absolute()))

project = "Upstox TOTP"
copyright = "2025, batpool"
author = "batpool"

release = "1.0.3"
version = "1.0.3"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.ifconfig",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_rtd_theme",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
]

templates_path = ["_templates"]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README.md"]

pygments_style = "sphinx"

html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "canonical_url": "",
    "analytics_id": "",
    "logo_only": False,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "vcs_pageview_mode": "",
    "style_nav_header_background": "#2980b9",
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

html_static_path = ["_static"]

html_sidebars = {
    "**": [
        "relations.html",
        "searchbox.html",
    ]
}


html_logo = "../assets/upstox-totp.png"


autodoc_member_order = "bysource"


autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
    "show-inheritance": True,
}


autodoc_inherit_docstrings = True


autodoc_typehints = "description"


intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    "requests": ("https://requests.readthedocs.io/en/latest/", None),
}


todo_include_todos = True


napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True


myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]


copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True


extlinks = {
    "issue": ("https://github.com/batpool/upstox-totp/issues/%s", "#%s"),
    "pr": ("https://github.com/batpool/upstox-totp/pull/%s", "PR #%s"),
    "pypi": ("https://pypi.org/project/%s/", "%s"),
}


autodoc_typehints_format = "short"


autoclass_content = "both"


def skip(app, what, name, obj, would_skip, options):
    if name == "__init__":
        return False
    return would_skip


def setup(app):
    app.connect("autodoc-skip-member", skip)

    app.add_css_file("custom.css")
