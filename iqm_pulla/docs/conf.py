# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# Find the path to the source files we want to to document, relative to the location of this file,
# convert it to an absolute path.
py_path = os.path.join(os.getcwd(), os.path.dirname(__file__), "../src")
sys.path.insert(0, os.path.abspath(py_path))

# -- Project information -----------------------------------------------------

project = "IQM Pulla"
author = "IQM Pulla developers"

# The short X.Y version.
version = ""
# The full version, including alpha/beta/rc tags.
release = ""
try:
    from iqm.pulla import __version__ as version
except ImportError:
    pass
else:
    release = version

copyright = "2024-2025, IQM Finland Oy, Release {}".format(release)

# -- General configuration ---------------------------------------------------

# require a recent version of Sphinx
needs_sphinx = "7.2"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.todo",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.bibtex",
    "myst_nb",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Include extra files in the HTML docs.
html_extra_path = []

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".*"]

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = "%Y-%m-%d"

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = True


# -- Autodoc ------------------------------------------------------------

# member ordering in autodoc output (default: 'alphabetical')
autodoc_member_order = "bysource"

# where should signature annotations appear in the docs, function signature or parameter description?
autodoc_typehints = "description"
# autodoc_typehints = 'description' puts the __init__ annotations into its docstring,
# which we thus have to include in the class documentation.
autoclass_content = "class"

# Sphinx 3.3+: manually clean up type alias rendering in the docs
# autodoc_type_aliases = {'TypeAlias': 'exa.experiment.somemodule.TypeAlias'}


# -- Autosummary ------------------------------------------------------------

# use autosummary to generate stub pages for API docs
autosummary_generate = True


# -- Options for HTML output -------------------------------------------------

import sphinx_book_theme

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_book_theme"

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = [sphinx_book_theme.get_html_theme_path()]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {}

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_static/images/logo.png"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "_static/images/favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%Y-%m-%d"

# Output file base name for HTML help builder.
htmlhelp_basename = "iqm_pulla-doc"


# -- MathJax options ----------------------------------------------------------

# Here we configure MathJax, mostly to define LaTeX macros.
mathjax3_config = {
    "tex": {
        "macros": {
            "vr": r"\vec{r}",  # no arguments
            "ket": [r"\left| #1 \right\rangle", 1],  # one argument
            "iprod": [r"\left\langle #1 | #2 \right\rangle", 2],  # two arguments
        }
    }
}


# -- External mapping ------------------------------------------------------------

python_version = ".".join(map(str, sys.version_info[0:2]))
intersphinx_mapping = {
    "python": ("https://docs.python.org/" + python_version, None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "iqm.station_control.client": (
        "../station-control-client",
        "../../station-control-client/build/sphinx/objects.inv",
    ),
    "iqm.station_control.interface": (
        "../station-control-client",
        "../../station-control-client/build/sphinx/objects.inv",
    ),
    "iqm.pulse": ("../iqm-pulse", "../../iqm-pulse/build/sphinx/objects.inv"),
    "exa.common": ("../exa-common", "../../exa-common/build/sphinx/objects.inv"),
    "iqm.iqm_client": ("../iqm-client", "../../iqm-client/build/sphinx/objects.inv"),
    "iqm.qiskit_iqm": ("../iqm-client", "../../iqm-client/build/sphinx/objects.inv"),
}

# update intersphinx_mapping so it reads inventory from gitlab pages, but
# generate links to the pages under local file path
# this is used only in `docs with generated links to local target` ci\cd job
use_local_target = os.getenv("USE_LOCAL_TARGET", "").lower()
if use_local_target == "true":
    intersphinx_mapping.update(
        {
            "iqm.station_control.client": (
                "../station-control-client",
                "https://iqm.gitlab-pages.iqm.fi/qccsw/exa/exa-repo/station-control-client/objects.inv",
            ),
            "iqm.station_control.interface": (
                "../station-control-client",
                "https://iqm.gitlab-pages.iqm.fi/qccsw/exa/exa-repo/station-control-client/objects.inv",
            ),
            "iqm.pulse": ("../iqm-pulse", "https://iqm.gitlab-pages.iqm.fi/qccsw/exa/exa-repo/iqm-pulse/objects.inv"),
            "exa.common": (
                "../exa-common",
                "https://iqm.gitlab-pages.iqm.fi/qccsw/exa/exa-repo/exa-common/objects.inv",
            ),
            "iqm.iqm_client": (
                "../iqm-client",
                "https://iqm.gitlab-pages.iqm.fi/qccsw/exa/exa-repo/iqm-client/objects.inv",
            ),
            "iqm.qiskit_iqm": (
                "../iqm-client",
                "https://iqm.gitlab-pages.iqm.fi/qccsw/exa/exa-repo/iqm-client/objects.inv",
            ),
        }
    )
else:
    extlinks = {
        "issue": ("https://jira.iqm.fi/browse/%s", "issue %s"),
        "mr": ("https://gitlab.iqm.fi/iqm/qccsw/exa/exa-repo/-/merge_requests/%s", "MR %s"),
    }

# -- Options for MyST-NB ---------------------------------------------------------
nb_execution_mode = "off"


# -- Options for sphinxcontrib.bibtex -------------------------------------------------

# List of all bibliography files used.
bibtex_bibfiles = ["references.bib"]
