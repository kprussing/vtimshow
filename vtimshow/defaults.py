#!/usr/bin/env python3
"""
Default parameters for the module.

"""
import logging
import os

logging.getLogger().addHandler(logging.NullHandler())

AUTHOR = "Keith F Prussing"
AUTHOR_EMAIL = "kprussing74@gmail.com"
LICENSE = "MIT"
PLUGIN_CLASS = "VtImageViewer"
PLUGIN_NAME = "Image Viewer"
COMMENT = "Display data sets as images"
VERSION = "{VERSION!s}"
UID = "image_viewer"
FOLDER, MODULE_NAME = os.path.split(os.path.dirname(__file__))

