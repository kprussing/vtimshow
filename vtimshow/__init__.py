#!/usr/bin/env python3
__doc__="""The top level module for the image viewer plugin to ViTables.

This package is a plugin for ViTables_ that allows viewing data sets as
images instead of tables of numbers.  The plugin can be activated under
the preferences menu in ViTables.

.. _ViTables: http://vitables.org

"""

# Module imports
import logging
import os
import pkg_resources

_defaults = dict(
    PLUGIN_CLASS = "VtImageViewer",
    PLUGIN_NAME = "Image Viewer",
)
_defaults["FOLDER"], _defaults["MODULE_NAME"] = os.path.split(
    os.path.dirname(__file__)
)
_defaults["LOGGER"] = logging.getLogger(_defaults["MODULE_NAME"])
_defaults["LOGGER"].addHandler(logging.NullHandler())
_dist = pkg_resources.get_distribution(_defaults["MODULE_NAME"])
_defaults["VERSION"] = _dist.version
pairs = (
    ("AUTHOR", "Author:"),
    ("AUTHOR_EMAIL", "Author-email:"),
    ("LICENSE", "License:"),
    ("COMMENT", "Summary:"),
    ("UID", "Name:")
)
_metadata = _dist.get_metadata("PKG-INFO")
for k1, k2 in pairs:
    _defaults[k1] = _metadata.split(k2)[1].split("\n")[0].strip()

__docformat__ = "restructuredtext"
__version__ = _defaults["VERSION"]

plugin_class = _defaults["PLUGIN_CLASS"]
plugin_name = _defaults["PLUGIN_NAME"]
comment = _defaults["COMMENT"]

from vtimshow.vtimageviewer import VtImageViewer

from .utils import setup_logger as _setup_logger
_setup_logger(_defaults["MODULE_NAME"])

