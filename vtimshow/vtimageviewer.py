#!/usr/bin/env python3
__doc__="""The module defining the interface class."""
import logging
import numpy

from PyQt4 import QtGui

import vitables
from vitables.vtapp import translate as _translate

from . import comment, dist, meta, plugin_class, plugin_name
from .imagewindow import ImageWindow
from .multicubemath import MultiCubeMath

class VtImageViewer:
    """The interface class needed by ViTables

    This is the high level class needed to plug into ViTables.  It
    adds the necessary menu options to the appropriate menu(s) and
    defines the methods to launch the desired actions.

    """
    UID = meta.split("Name:")[1].split("\n")[0].strip()
    NAME = plugin_name
    COMMENT = comment

    def __init__(self, parent=None):
        """Add the menu items and connect the actions."""
        logger = logging.getLogger(__name__ +".VtImageViewer")
        logger.debug("Constructor called")

        gui = vitables.utils.getGui()
        actions = []

        action = QtGui.QAction(
            _translate(
                plugin_class, "Image View", "Plugin action"
            ),
            gui
        )
        actions.append(action)
        actions[-1].setStatusTip(_translate(
            plugin_class, "View as image", "Plugin action"
        ))
        actions[-1].triggered.connect(self.imshow)

        action = QtGui.QAction(
            _translate(
                plugin_class, "Compare Datasets", "Plugin action"
            ),
            gui
        )
        actions.append(action)
        actions[-1].setStatusTip(_translate(
            plugin_class, "Begin comparing datasets", "Plugin tool tip"
        ))
        actions[-1].triggered.connect(self.launch_compare)

        vitables.utils.addToLeafContextMenu(actions)

    def imshow(self):
        """Generate an image from a dataset in the workspace."""
        logger = logging.getLogger(__name__ +".VtImageViewer.imshow")
        indexes = vitables.utils.getSelectedIndexes()
        if len(indexes) != 1:
            msg = _translate(
                plugin_class,
                "Only one node can be viewed as an image at a time!",
                "Plugin error message"
            )
            logger.error(msg)
            return

        dbg = vitables.utils.getGui().dbs_tree_model
        leaf = dbg.nodeFromIndex(indexes[0])
        node = leaf.node
        if node.dtype.kind not in "iuf":
            msg = _translate(
                plugin_class,
                "Node must be a numeric type array!",
                "Plugin error message"
            )
            logger.error(msg)
            return

        if not (node.ndim == 2 and 1 not in node.shape) \
                and node.ndim not in (3,4):
            msg = _translate(
                plugin_class,
                "Node must be 2D, 3D or 4D.",
                "Plugin error message"
            )
            logger.error(msg)
            return

        workspace = vitables.utils.getGui().workspace

        window = ImageWindow(leaf, parent=workspace)

    def launch_compare(self):
        """Launch the multiple dataset comparison."""
        workspace = vitables.utils.getGui().workspace
        window = MultiCubeMath(parent=workspace)

    def helpAbout(self, parent):
        """Full description of the plugin.

        The help/about page needed by ViTables to recognize a plugin.
        This has been adapted from the code used in :class:`ImportCSV`
        distributed with ViTables.

        Parameters
        ----------

        parent : :class:`PyQt4.QtGui.QWidget`
            The parent object provided by ViTables

        """
        from .aboutpage import AboutPage
        author = "{0:s} <{1:s}>".format(
            meta.split("Author:")[1].split("\n")[0].strip(),
            meta.split("Author-email:")[1].split("\n")[0].strip(),
        )
        desc = {
            "version" : dist.version,
            "module_name" : dist.project_name,
            "folder" : dist.location,
            "author" : author,
            "comment" : _translate(
                plugin_class,
                """
                <qt>
                <p>View datasets as images.</p>
                <p>
                If the dataset is simply 2D, view it as an image.  If
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

