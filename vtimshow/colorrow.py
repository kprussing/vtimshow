#!/usr/bin/env python3
__doc__="""The module defining :class:`ColorRow`."""
import logging
import os

import pyqtgraph

from PyQt4 import QtCore
from PyQt4 import QtGui

import tables
import vitables
from vitables.vtapp import translate as _translate

from . import _defaults
from .preferences import Preferences
from .filters import Filters

class ColorRow(QtGui.QGroupBox):
    """A class to hold a row for assigning the color channels.

    This is a group divided into four columns.  The first is a combo box
    listing all of the available leaf nodes open in the application.
    The middle column is a PyQtGraph horizontal axis analogous to the
    :class:`pyqtgraph.ImageView.roiPlot` with a vertical line for
    selecting the frame.  The third column is a spin box connected to
    the horizontal selector in the middle.  The fourth column is a combo
    box to select an extension to applying RGB weights to the data
    cubes.

    ..  note::  The current implementation does not allow for reshaping
                the data sets.  The *must* be stored in the order listed
                in the :class:`preferences.Preferences`.

    Parameters
    ----------

    parent : :class:`PyQt4.QtGui.QWidget`
        The parent object.  Most likely the MultiCubeMath window.
    index : ViTables index
        The index of the leaf node to process.
    color : string
        The pyqtgraph color of the line in the horizontal selector.

    """
    frame_changed = QtCore.Signal()
    """Signal that the frame changed on a row."""

    def __init__(self, parent, index=None, color=None):
        """Initialize the color row group."""
        logger = logging.getLogger(__name__ +".ColorRow")
        super(ColorRow, self).__init__(parent)

        #self._group = QtGui.QGroupBox(self)
        self._layout = QtGui.QGridLayout(self)
        self._layout.setMargin(0)
        self._layout.setSpacing(0)

        self._combo_box = QtGui.QComboBox(self)
        self._combo_box.addItem("")
        self._layout.addWidget(self._combo_box, 0, 0, 1, 1)

        self._plot = pyqtgraph.PlotWidget(self)
        self._line = pyqtgraph.InfiniteLine(0, movable=True)
        self._line.setPen(color)
        self._plot.hideAxis("left")
        self._plot.addItem(self._line)
        self._layout.addWidget(self._plot, 0, 1, 1, 1)

        self._spin_box = QtGui.QSpinBox(self)
        self._layout.addWidget(self._spin_box, 0, 2, 1, 1)

        self._filter = Filters(self)
        self._filter.setEnabled(False)
        self._layout.addWidget(self._filter, 0, 3, 1, 1)

        self._layout.setColumnStretch(0, 2)
        self._layout.setColumnStretch(1, 3)
        self._layout.setColumnStretch(2, 1)
        self._layout.setColumnStretch(3, 1)

        self._combo_box.currentIndexChanged.connect(self._node_changed)
        self._line.sigPositionChanged.connect(self._line_moved)
        self._spin_box.valueChanged.connect(self._spin_changed)
        self._filter.currentIndexChanged.connect(
            self.frame_changed.emit
        )

        self._order = Preferences()

        self._update_combobox()
        if index is None:
            self._node_changed()
        else:
            dbs = vitables.utils.getGui().dbs_tree_model
            node = dbs.nodeFromIndex(index).node
            filename = os.path.split(node._v_file.filename)[-1]
            nodepath = node._v_pathname
            label = "{0:s} {1:s}".format(filename, nodepath)

            idx = self._combo_box.findText(label)
            self._combo_box.setCurrentIndex(idx)
            #print(node.__dir__())

        logger.debug("Index type {0!s}".format(index))

    def _update_combobox(self):
        """Update the combo box with the current open files."""
        # The open files can be found from the data base tree model in
        # the GUI.
        gui = vitables.utils.getGui()
        databases = gui.dbs_tree_model
        groups = (tables.group.RootGroup, tables.group.Group)
        for filename in databases.getDBList():
            db = databases.getDBDoc(filename)
            for nodepath in db.listNodes():
                node = db.getNode(nodepath)
                if isinstance(node, groups):
                    continue

                if node.dtype.kind not in "iuf":
                    continue

                if node.ndim not in (2,3,4):
                    continue

                label = "{0:s} {1:s}".format(db.filename, nodepath)
                if self._combo_box.findText(label) == -1:
                    self._combo_box.addItem(label, node)

    def _node_changed(self):
        """Update the current node.

        If the current node has been changed, check to see if we now
        have a 3D or 4D image and activate the sliders and filter combo
        box.  Otherwise, deactivate them for a simple monochrome image.

        """
        logger = logging.getLogger(__name__ +".ColorRow._node_changed")
        index = self._combo_box.currentIndex()
        self.data = self._combo_box.itemData(index)
        self._spin_box.setValue(0)
        if self.data is not None and len(self.data.shape) > 2:
            if len(self.data.shape) == 3:
                depth = int(self._order["3D"]["Depth"])
            elif len(self.data.shape) == 4:
                depth = int(self._order["3D"]["Depth"])
            else:
                raise RuntimeError("This should be impossible")

            self._plot.setEnabled(True)
            self._spin_box.setEnabled(True)
            self._plot.setXRange(0, self.data.shape[depth])
            self._spin_box.setMaximum(self.data.shape[depth])
            if self.node_is_2d() or self.data.ndim == 4:
                self._filter.setEnabled(False)
            else:
                self._filter.setEnabled(True)
        else:
            self._line.setEnabled(False)
            self._plot.setEnabled(False)
            self._spin_box.setEnabled(False)
            self._filter.setEnabled(False)

        logger.debug("Node type {0!s}".format(self.data))
        #logger.debug("Node path {0!s}".format(self.data._v_pathname))

    def _line_moved(self):
        """Make the line and combo box track each other."""
        self._spin_box.setValue(int(self._line.value()))

    def _spin_changed(self):
        """Make the line and combo box track each other."""
        self._line.setValue(self._spin_box.value())
        self.frame_changed.emit()

    def node_is_2d(self):
        """Determine if the node is a 2D image.

        The easiest answer is if the node has only two dimensions.  If
        the node has three dimensions and the RGB(A) dimension in the
        preferences is three of four, then it is also 2D.

        """
        rgba = int(self._order["2D"]["RGB(A)"])
        if self.data is None:
            return False
        elif self.data.ndim == 2:
            return True
        elif self.data.ndim == 3 and self.data.shape[rgba] in (3,4):
            return True
        else:
            return False

    def get_frame(self):
        """Return the currently selected frame.

        Load the data set into memory from file.  If the array is a
        monochrome or RGB(A) 2D image, simply return it.  If the image
        is 4D, select the frame from the spin box and return that frame.
        Otherwise, if the image is a (N,H,W) array, apply the selected
        filter.  If the filter returns ``None``, get the index from the
        spin box and return that frame.

        """
        if self.data is None:
            return None

        idx = self._spin_box.value()
        if self.data.ndim == 2:
            array = self.data.transpose((
                int(self._order["2D"]["Height"]),
                int(self._order["2D"]["Width"])
            ))
            ret = array
        elif self.data.ndim == 3:
            if self.node_is_2d():
                array = self.data.transpose((
                    int(self._order["2D"]["Height"]),
                    int(self._order["2D"]["Width"]),
                    int(self._order["2D"]["RGB(A)"])
                ))
                ret = array
            else:
                array = self.data.transpose((
                    int(self._order["3D"]["Depth"]),
                    int(self._order["3D"]["Height"]),
                    int(self._order["3D"]["Width"])
                ))
                ret = self._filters.apply(array)
        else:
            array = self.data.transpose((
                int(self._order["4D"]["Depth"]),
                int(self._order["4D"]["Height"]),
                int(self._order["4D"]["Width"]),
                int(self._order["4D"]["RGB(A)"])
            ))
            ret = array[idx, :, :, :]

        if ret is None:
            idx = self._spin_box.value()
            ret = array[idx, :, :]

        return ret

