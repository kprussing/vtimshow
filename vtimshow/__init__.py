#!/usr/bin/env python3

# Module imports
import logging
import os
import pkg_resources

import vitables

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

def _setup_logger(name):
    """
    Add the GUI's logging window as a stream handler.

    By default, the stream logger is removed during the invocation of
    ``vitables``.  The logging window in the GUI is a stream handler for
    the ``vitables`` logger _only_.  This method will add the logging
    window in the GUI as a stream handler for the named logger.  The
    method checks to see if ``vitables`` is an active application.  If
    it is not, nothing is done.

    """
    logger = logging.getLogger(name)
    app = vitables.utils.getApp()
    if app is not None:
        stream = logging.StreamHandler(app.gui.logger)
        stream.setFormatter(
            logging.Formatter(vitables.vtgui._GUI_LOG_FORMAT)
        )
        logger.addHandler(stream)

    return

_setup_logger(_defaults["MODULE_NAME"])

