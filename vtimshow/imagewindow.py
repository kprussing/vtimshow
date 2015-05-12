#!/usr/bin/env python3
import logging
import numpy

from PyQt4 import QtCore
from PyQt4 import QtGui

import pyqtgraph

from vitables.vtapp import translate

from . import _defaults
from .setdims import SetDims

class ImageWindow(QtGui.QMdiSubWindow):
    """
    The window to hold the image.
    """

    def __init__(self, leaf, parent):
        logger = logging.getLogger(__name__ +".ImageWindow")
        if leaf.node.ndim in (2,3):
            data = leaf.node.read()
        else:
            msg = translate(
                    _defaults["PLUGIN_CLASS"],
                    "Array must be 2D or 3D",
                    "Plugin error message"
                )
            logger.error(msg)
            raise RuntimeError(msg)

        dims = SetDims(data)
        if dims.exec() == dims.Rejected:
            return

        super(ImageWindow, self).__init__(parent)

        # Prepare the image array
        W = dims.get_width()
        H = dims.get_height()
        D = dims.get_depth()
        if D is None:
            dat = data.transpose((W.dim, H.dim))[
                    W.start:W.end:W.stride,
                    H.start:H.end:H.stride
            ]
        else:
            dat = data.transpose((D.dim, W.dim, H.dim))[
                    D.start:D.end:D.stride,
                    W.start:W.end:W.stride,
                    H.start:H.end:H.stride
            ]

        dat[numpy.isnan(dat)] = 0

        widget = pyqtgraph.ImageView()
        widget.setImage(dat)
        self.setWidget(widget)
        widget.show()

        self.pindex = None
        self.dbt_leaf = leaf

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle(self.dbt_leaf.name)

