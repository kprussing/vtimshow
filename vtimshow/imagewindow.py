#!/usr/bin/env python3
import logging
import numpy

from PyQt4 import QtCore
from PyQt4 import QtGui

import pyqtgraph

from vitables.vtapp import translate

from . import _defaults

class ImageWindow(QtGui.QMdiSubWindow):
    """
    The window to hold the image.
    """

    def __init__(self, leaf, parent):
        logger = logging.getLogger(__name__ +".ImageWindow")
        if leaf.node.ndim == 2:
            data = leaf.node.read()
        elif leaf.node.ndim == 3:
            data = leaf.node.read().transpose((2,0,1))
        else:
            msg = translate(
                    _defaults["PLUGIN_CLASS"],
                    "Array must be 2D or 3D",
                    "Plugin error message"
                )
            logger.error(msg)
            raise RuntimeError(msg)

        super(ImageWindow, self).__init__(parent)
        data[numpy.isnan(data)] = 0
        widget = pyqtgraph.ImageView()
        widget.setImage(data)
        self.setWidget(widget)
        widget.show()

        self.pindex = None
        self.dbt_leaf = leaf

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle(self.dbt_leaf.name)

