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

