# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import os
import sys
sys.path.insert(0, os.path.abspath('doc-shared/code'))
sys.path.insert(0, os.path.abspath('.'))

# -- Shared settings -----------------------------------------------------

# These environment variable establish base names that are used in sharedconf.py
#   BASE_DIR holds base directory for this project
#   EPI_PROJECT holds the base name for this project
#   EPI_TITLE holds the document title for this project
#   EPI_SHORT_TITLE holds the short title for use in URLs or other references
os.environ['BASE_DIR'] = os.getcwd()
os.environ['EPI_PROJECT'] = str('fred-tutorials')
os.environ['EPI_TITLE'] = str('FRED Tutorials')
os.environ['EPI_SHORT_TITLE'] = str('tutorials')

from sharedconf import *

# -- Custom settings -----------------------------------------------------
# You can override the shared defaults here, if necessary

# Allow markdown files as well as reStructuredText
source_suffix = ['.rst', '.md']

# Adjust extensions and include patterns for the tutorials
extensions.append('sphinx.ext.imgmath')
exclude_patterns.remove('README.md')
exclude_patterns.remove('README.rst')

# Turn on the GitHub link, since this is a public repository
html_context = {
  'display_github': True,
}
