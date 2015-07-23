#!/usr/bin/env python3
__doc__="""The module defining the image window widget."""
import logging
import numpy

from PyQt4 import QtCore
from PyQt4 import QtGui

import pyqtgraph

import vitables
from vitables.vtapp import translate

from . import _defaults
from .setdims import SetDims
from .preferences import Preferences

class ImageWindow(QtGui.QMdiSubWindow):
    """The window to hold the image in the workspace of ViTables

    This class defines the widget to live within the ViTables workspace
    and instantiates a :class:`pyqtgraph.ImageView` to display the data
    set.  The data set is loaded from the underlying file in the order
    specified by :class:`preferences.Preferences`.  This also adds a
    menu item to launch a :class:`setdims.SetDims` window to reshape the
    array if the underlying order of the data set is not what is
    specified in the preferences.

    """

    def __init__(self, leaf, parent):
        """Load the data set and display it as an image.

        Parameters
        ----------

        leaf : :class:`vitables.h5db.leafnode`
            The leaf tree node to view
        parent : :class:`PyQt4.QtGui.QMdiArea`
            The workspace from ViTables

        """
        logger = logging.getLogger(__name__ +".ImageWindow")
        if leaf.node.ndim in (2,3,4):
            data = leaf.node.read()
        else:
            msg = translate(
                    _defaults["PLUGIN_CLASS"],
                    "Array must be 2D, 3D, or 4D",
                    "Plugin error message"
                )
            logger.error(msg)
            raise RuntimeError(msg)

        super(ImageWindow, self).__init__(parent)

        config = Preferences()
        if leaf.node.ndim == 2:
            self.data = data.transpose((
                int(config["2D"]["Height"]),
                int(config["2D"]["Width"])
            ))
        elif leaf.node.ndim == 3:
            if data.shape[int(config["2D"]["RGB(A)"])] in (3,4):
                self.data = data.transpose((
                    int(config["2D"]["Height"]),
                    int(config["2D"]["Width"]),
                    int(config["2D"]["RGB(A)"])
                ))
            else:
                self.data = data.transpose((
                    int(config["3D"]["Depth"]),
                    int(config["3D"]["Height"]),
                    int(config["3D"]["Width"])
                ))
        else:
            self.data = data.transpose((
                int(config["4D"]["Depth"]),
                int(config["4D"]["Height"]),
                int(config["4D"]["Width"]),
                int(config["4D"]["RGB(A)"])
            ))

        self.image = pyqtgraph.ImageView()
        self.image.setImage(self.data)
        self.setWidget(self.image)
        self.image.show()

        self.pindex = None
        self.dbt_leaf = leaf

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle(self.dbt_leaf.name)

        if self.image.menu is None:
            self.image.buildMenu()

        action = QtGui.QAction("Reshape", self.image.menu)
        vitables.utils.addToMenu(self.image.menu, action)
        action.triggered.connect(self.reshape)

    def reshape(self):
        """Select different axis for displaying the image."""
        logger = logging.getLogger(__name__ +".ImageWindow.reshape")
        dims = SetDims(self.data)
        if dims.exec() == dims.Rejected:
            return

        # Prepare the image array
        W = dims.get_width()
        logger.debug("Width  : {0!s}".format(W))
        H = dims.get_height()
        logger.debug("Height : {0!s}".format(H))
        D = dims.get_depth()
        logger.debug("Depth  : {0!s}".format(D))
        R = dims.get_rgba()
        logger.debug("RGBA   : {0!s}".format(R))
        if D is None and R is None:
            data = self.data.transpose((W.dim, H.dim))[
                W.start:W.end:W.stride,
                H.start:H.end:H.stride
             ]
        elif D is not None and R is None:
            if len(self.data.shape) != 3:
                msg = translate(
                    _defaults["PLUGIN_CLASS"],
                    "Either Depth or RGBA can be set!  Not both.",
                    "Plugin error message"
                )
                logger.error(msg)
                return

            data = self.data.transpose((D.dim, W.dim, H.dim))[
                D.start:D.end:D.stride,
                W.start:W.end:W.stride,
                H.start:H.end:H.stride
            ]
        elif D is None and R is not None:
            if len(self.data.shape) != 3:
                msg = translate(
                    _defaults["PLUGIN_CLASS"],
                    "Either Depth or RGBA can be set!  Not both.",
                    "Plugin error message"
                )
                logger.error(msg)
                return

            data = self.data.transpose((W.dim, H.dim, R.dim))[
                W.start:W.end:W.stride,
                H.start:H.end:H.stride,
                :
            ]
        elif D is not None and R is not None:
            data = self.data.transpose((D.dim, W.dim, H.dim, R.dim))[
                D.start:D.end:D.stride,
                W.start:W.end:W.stride,
                H.start:H.end:H.stride,
                :
            ]
        else:
            raise RuntimeError("This should never be possible")


        self.image.setImage(data)
        self.image.show()
        return

