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

from .preferences import Preferences
from .filters import Filters
from .filters.nofilter import name as _no_filter_name

class ColorRow(QtGui.QGroupBox):
    """A class to hold a row for assigning the color channels.

    This is a Qt group divided into four columns.  The first is a combo
    box listing all of the available leaf nodes open in the application.
    The middle column is a PyQtGraph horizontal axis analogous to the
    :class:`pyqtgraph.ImageView.roiPlot` with a vertical line for
    selecting the frame.  The third column is a spin box connected to
    the horizontal selector in the middle.  The fourth column is a combo
    box to select an extension to apply a ``vtimshow.filters`` filter to
    the dataset.

    ..  note::  The current implementation does not allow for reshaping
                the datasets.  The *must* be stored in the order listed
                in the :class:`preferences.Preferences`.

    """
    frame_changed = QtCore.Signal()
    """Signal that the frame changed on a row."""

    def __init__(self, parent, index=None, color=None):
        """Initialize the color row group.

        Parameters
        ----------

        parent : :class:`MultiCubeMath`
            The window that will hold the color row.
        index : :class:`PyQt4.QtCore.QModelIndex` or ``None``
            The index of a dataset in a revealed group.
        color : string
            A valid color parameter to pass to PyQtGraph.

        """
        logger = logging.getLogger(__name__ +".ColorRow")
        super(ColorRow, self).__init__(parent)

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

        self._filters = Filters(self)
        self._filters.setEnabled(False)
        self._layout.addWidget(self._filters, 0, 3, 1, 1)

        self._layout.setColumnStretch(0, 2)
        self._layout.setColumnStretch(1, 3)
        self._layout.setColumnStretch(2, 1)
        self._layout.setColumnStretch(3, 1)

        self._combo_box.currentIndexChanged.connect(self._node_changed)
        self._line.sigPositionChanged.connect(self._line_moved)
        self._spin_box.valueChanged.connect(self._spin_changed)
        self._filters.currentIndexChanged.connect(self._filter_changed)

        self._order = Preferences()
        self.cached = False

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
        """Update the combo box with the currently expanded groups.

        Traverse the tree model and populate the dataset combo box with
        the leaf names of the leaf datasets that are currently open or
        have been opened and placed into the ViTables index model.  We
        do this because ViTables does not establish the
        :class:`PyQt4.QtCore.QModelIndex` of a leaf node until it has
        been expanded in the tree viewer.  This is reasonable because
        the users will most likely want to compare datasets from
        closely related groups.  The down side is the user must expand
        the group tree out to the leafs before it will be populated in
        the combo box.

        """
        # The open files can be found from the database tree model in
        # the GUI.
        logger = logging.getLogger(
            __name__ +".ColorRow._update_combobox"
        )
        gui = vitables.utils.getGui()
        databases = gui.dbs_tree_model

        # Put the root objects onto the stack.  These represent the file
        # objects in the tree.  We also include a boolean to flag that
        # this item has not been touched.
        stack = [
            (index, False) for index in
            databases.indexChildren(QtCore.QModelIndex())
        ]
        groups = (tables.group.RootGroup, tables.group.Group)
        while len(stack) > 0:
            # Pop an index and flag out of the stack.
            index, seen = stack.pop()
            node = databases.nodeFromIndex(index)
            if node.name == "Query results":
                # Ignore the query results.
                continue

            if seen or not databases.hasChildren(index):
                #logger.debug("Node type {0!s}".format(node))
                # If the index does not have children or we have already
                # seen this item, process it.
                if isinstance(node.node, groups):
                    # Skip the root and group nodes.  We have already
                    # reviewed the children.
                    continue

                if node.node.dtype.kind not in "iuf":
                    # It must be a numeric array
                    continue

                if node.node.ndim not in (2,3,4):
                    # Make sure it can be an image.
                    continue

                label = "{0:s} {1:s}".format(
                    os.path.split(node.node._v_file.filename)[-1],
                    node.node._v_pathname
                )
                if self._combo_box.findText(label) == -1:
                    self._combo_box.addItem(label, index)

                #logger.debug("Node: {0!s}".format(node.name))
            else:
                # Before we process this index, mark it as seen and
                # process its children.
                stack.append((index, True))
                for idx in databases.indexChildren(index):
                    stack.append((idx, False))

    def _node_changed(self):
        """Update the current node.

        If the current node has been changed, check to see if we now
        have a 3D or 4D image and activate the sliders and filter combo
        box.  Otherwise, deactivate them for a simple monochrome image.

        """
        logger = logging.getLogger(__name__ +".ColorRow._node_changed")
        databases = vitables.utils.getGui().dbs_tree_model
        index = self._combo_box.currentIndex()
        self.index = self._combo_box.itemData(index)
        #logger.debug("Index type {0!s}".format(self.index))
        if self.index is None:
            self.data = None
        else:
            self.data = databases.nodeFromIndex(self.index).node

        #logger.debug("Node type {0!s}".format(self.data))
        self._spin_box.setValue(0)
        if self.data is not None and len(self.data.shape) > 2:
            if len(self.data.shape) == 3:
                depth = int(self._order["3D"]["Depth"])
            elif len(self.data.shape) == 4:
                depth = int(self._order["3D"]["Depth"])
            else:
                raise RuntimeError("This should be impossible")

            if self.node_is_2d():
                self._plot.setEnabled(False)
                self._spin_box.setEnabled(False)
            else:
                self._plot.setEnabled(True)
                self._spin_box.setEnabled(True)
                self._plot.setXRange(0, self.data.shape[depth])
                self._spin_box.setMaximum(self.data.shape[depth])

            if self.node_is_2d() or self.data.ndim == 4:
                self._filters.setEnabled(False)
            else:
                self._filters.setEnabled(True)
        else:
            self._line.setEnabled(False)
            self._plot.setEnabled(False)
            self._spin_box.setEnabled(False)
            self._filters.setEnabled(False)

        self.cached = False
        self.frame_changed.emit()

    def _line_moved(self):
        """Make the line and combo box track each other."""
        self._spin_box.setValue(int(self._line.value()))
        self.cached = False
        self.frame_changed.emit()

    def _spin_changed(self):
        """Make the line and combo box track each other."""
        self._line.setValue(self._spin_box.value())

    def _filter_changed(self):
        """"Disable the band selection if a filter is selected."""
        self._line.setEnabled(
            self._filters.currentText() == _no_filter_name
        )
        self._plot.setEnabled(
            self._filters.currentText() == _no_filter_name
        )
        self._spin_box.setEnabled(
            self._filters.currentText() == _no_filter_name
        )
        self.cached = False
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

        Load the dataset into memory from file if it is not currently
        cached.  If the array is a monochrome or RGB(A) 2D image, simply
        return it.  If the image is 4D, select the frame from the spin
        box and return that frame.  Otherwise, if the image is a (N,H,W)
        array, apply the selected filter.  If the filter returns
        ``None``, get the index from the spin box and return that frame.

        """
        logger = logging.getLogger(__name__ +".ColorRow.get_frame")
        if self.data is None:
            return None

        idx = self._spin_box.value()
        if not self.cached:
            logger.debug("Recomputing the array")
            self.filtered = False
            if self.data.ndim == 2:
                self._array = self.data.read().transpose((
                    int(self._order["2D"]["Height"]),
                    int(self._order["2D"]["Width"])
                ))
                logger.debug("Found 2D array!")
            elif self.data.ndim == 3:
                if self.node_is_2d():
                    self._array = self.data.read().transpose((
                        int(self._order["2D"]["Height"]),
                        int(self._order["2D"]["Width"]),
                        int(self._order["2D"]["RGB(A)"])
                    ))
                    self.filtered = True
                    logger.debug("Found 2D array!")
                else:
                    self._array = self.data.read().transpose((
                        int(self._order["3D"]["Depth"]),
                        int(self._order["3D"]["Height"]),
                        int(self._order["3D"]["Width"])
                    ))
                    ret = self._filters.apply(self._array)
                    if ret is not None:
                        self._array = ret
                        self.filtered = True
                    logger.debug("Found 3D array!")
            else:
                self._array = self.data.read().transpose((
                    int(self._order["4D"]["Depth"]),
                    int(self._order["4D"]["Height"]),
                    int(self._order["4D"]["Width"]),
                    int(self._order["4D"]["RGB(A)"])
                ))
                logger.debug("Found 4D array!")

            self.cached = True

        if self.data.ndim == 4:
            ret = self._array[idx,:,:,:]
        elif self.data.ndim == 3 and not self.filtered:
            ret = self._array[idx,:,:]
        else:
            ret = self._array

        return ret

