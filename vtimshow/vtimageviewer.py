#!/usr/bin/env python3
import logging
logging.getLogger().addHandler(logging.NullHandler())

from vtimshow import _defaults

from PyQt4 import QtGui

class VtImageViewer:
    """
    """
    UID = _defaults["UID"]
    NAME = _defaults["PLUGIN_NAME"]
    COMMENT = _defaults["COMMENT"]

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
            "module_name" : _defaults["MODULE_NAME"],
            "folder" : _defaults["FOLDER"],
            "author" : "{0:s} <{1:s}>".format(
                _defaults["AUTHOR"], _defaults["AUTHOR_EMAIL"]
            ),
            "comment" : translate(
                _defaults["PLUGIN_CLASS"],
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

