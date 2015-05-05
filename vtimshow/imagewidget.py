#!/usr/bin/env python3
import collections
import logging
import numpy

from PyQt4 import QtGui

# Importing PyQtGraph raises a warning on OSX about buggy behavior when
# the QApplication has already been started.  It appears to only occur
# under OSX so I'm not going to worry about it.
import pyqtgraph 

from vitables.vtapp import translate

from . import _defaults

# Define a named tuple for the ``dbt_leaf`` data.
DBTLeaf = collections.namedtuple(
    "DBTLeaf", ("filename",)
)

class ImageWidget(pyqtgraph.ImageView):
    """
    The widget to hold the image.
    """

    def __init__(self, node, parent=None):
        logger = logging.getLogger(__name__ +".ImageWidget")
        if node.ndim == 2:
            data = node.read()
        elif node.ndim == 3:
            data = node.read().transpose((2,0,1))
        else:
            msg = translate(
                _defaults["PLUGIN_CLASS"],
                "Node must be 2D or 3D.",
                "Plugin error message"
            )
            raise RuntimeError(msg)

        super(ImageWidget, self).__init__(parent)
        data[numpy.isnan(data)] = 0
        self.setImage(data)
        self.show()

        self.dbt_leaf = DBTLeaf(filename = node._v_file.filename)

