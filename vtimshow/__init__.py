#!/usr/bin/env python3

# Module imports
import logging
import os

import vitables

_defaults = dict(
    AUTHOR = "Keith F Prussing",
    AUTHOR_EMAIL = "kprussing74@gmail.com",
    LICENSE = "MIT",
    PLUGIN_CLASS = "VtImageViewer",
    PLUGIN_NAME = "Image Viewer",
    COMMENT = "Display data sets as images",
    VERSION = "{VERSION!s}",
    UID = "image_viewer"
)
_defaults["FOLDER"], _defaults["MODULE_NAME"] = os.path.split(
    os.path.dirname(__file__)
)
_defaults["LOGGER"] = logging.getLogger(_defaults["MODULE_NAME"])
_defaults["LOGGER"].addHandler(logging.NullHandler())

__docformat__ = "restructuredtext"
__version__ = _defaults["VERSION"]

plugin_class = _defaults["PLUGIN_CLASS"]
plugin_name = _defaults["PLUGIN_NAME"]
comment = _defaults["COMMENT"]

from vtimshow.vtimageviewer import VtImageViewer

