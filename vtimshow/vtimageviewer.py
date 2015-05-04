#!/usr/bin/env python3
import logging
logging.getLogger().addHandler(logging.NullHandler())

from . import defaults
from . import __version__

from PyQt4 import QtGui

class VtImageViewer:
    """
    """
    UID = defaults.UID
    NAME = defaults.PLUGIN_NAME
    COMMENT = defaults.COMMENT

    def __init__(self, parent=None):
        #super(VtImageViewer, self).__init__(parent)
        logger = logging.getLogger(__name__ +".VtImageViewer")
        logger.debug("Constructor called")

    def helpAbout(self, parent):
        """Full description of the plugin.

        This is adapted from the code used in the ``ImportCSV`` class
        distributed with ViTables.
        """
        from vitables.plugins.aboutpage import AboutPage
        desc = {
            "version" : __version__,
            "module_name" : defaults.MODULE_NAME,
            "folder" : defaults.FOLDER,
            "author" : "{0:s} <{1:s}>".format(
                defaults.AUTHOR, defaults.AUTHOR_EMAIL
            ),
            "comment" : QtGui.QApplication.translate(
                defaults.PLUGIN_CLASS,
                """
                <qt>
                <p>View 2D data set as an image.</p>
                <p>
                If the data set is simply 2D, view it as an image.  If
                the dataset is 3D of dimension (N,M,K), view each (N,M)
                slice [0,K) as an image with a slider.
                </p>
                </qt>
                """,
                "Text of an About plugin message box"
            )
        }
        about_page = AboutPage(desc, parent)
        return about_page

