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

dist = pkg_resources.get_distribution(__name__)
meta = dist.get_metadata(dist.PKG_INFO)

plugin_class = "VtImageViewer"
plugin_name = "Image Viewer"
comment = meta.split("Summary:")[1].split("\n")[0].strip()
module_name = __name__

logger = logging.getLogger(__name__).addHandler(logging.NullHandler())

__docformat__ = "restructuredtext"
__version__ = dist.version

from vtimshow.vtimageviewer import VtImageViewer

from .utils import setup_logger as _setup_logger
_setup_logger(__name__)

