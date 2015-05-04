#!/usr/bin/env python3
import logging
logging.getLogger().addHandler(logging.NullHandler())

from . import defaults

__docformat__ = "restructuredtext"
__version__ = defaults.VERSION

plugin_class = defaults.PLUGIN_CLASS
plugin_name = defaults.PLUGIN_NAME
comment = defaults.COMMENT

from .vtimageviewer import VtImageViewer

