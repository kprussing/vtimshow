#!/usr/bin/env python3
import logging
import numpy

from PyQt4 import QtGui

import vitables
from vitables.vtapp import translate

from . import _defaults
from .imagewindow import ImageWindow

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

        gui = vitables.utils.getGui()
        action = QtGui.QAction("Image View", gui)
        action.setStatusTip("View as image")
        action.triggered.connect(self.imshow)

        vitables.utils.addToLeafContextMenu(action)

    def imshow(self):
        """
        Generate the image.
        """
        logger = logging.getLogger(__name__ +".VtImageViewer.imshow")
        indexes = vitables.utils.getSelectedIndexes()
        if len(indexes) != 1:
            msg = translate(
                _defaults["PLUGIN_CLASS"],
                "Only one node can be viewed as an image at a time!",
                "Plugin error message"
            )
            logger.error(msg)
            return

        dbg = vitables.utils.getGui().dbs_tree_model
        leaf = dbg.nodeFromIndex(indexes[0])
        node = leaf.node
        valid = numpy.issubdtype(node.dtype, int) | \
                numpy.issubdtype(node.dtype, float)
        if not valid:
            msg = translate(
                _defaults["PLUGIN_CLASS"],
                "Node must be a numeric type array!",
                "Plugin error message"
            )
            logger.error(msg)
            return

        if not (node.ndim == 2 and 1 not in node.shape) \
                and node.ndim != 3:
            msg = translate(
                _defaults["PLUGIN_CLASS"],
                "Node must be 2D or 3D.",
                "Plugin error message"
            )
            logger.error(msg)
            return

        workspace = vitables.utils.getGui().workspace

        window = ImageWindow(leaf, parent=workspace)

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

