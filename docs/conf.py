import os
import sys

# -- Project information -------------------------------------------------------
project = 'Seeed studio STM32MP135D BSP using ST stack'
author = 'Jakub Buczynski <KubaTaba1uga>'

# -- General configuration -----------------------------------------------------
extensions = [
    'breathe',
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "myst_parser",
]

# Tell Breathe where the Doxygen XML is
breathe_projects = {
    "STM32MP135F eBook Reader": os.path.abspath(os.path.join('..', 'build', 'doxygen', 'xml')),
}
breathe_default_project = "Seeed studio STM32MP135D BSP using ST stack"

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output ---------------------------------------------------
html_theme = "sphinx_rtd_theme"


html_theme_options = {
}

html_context = {
    "display_github": True,
    "github_user": "KubaTaba1uga",
    "github_repo": "st_bsp_stm32mp135d_seeed_studio",
    "github_version": "master",
    "conf_py_path": "/docs/",
}

html_short_title = "Seeed studio STM32MP135D BSP"
pygments_style = "monokai"
pygments_dark_style = "monokai"

copyright = "2025, Jakub Buczynski <KubaTaba1uga>"
