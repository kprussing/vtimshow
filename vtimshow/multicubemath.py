#!/usr/bin/env python3
__doc__="""The module defining :class:`MultiCubeMath`."""

import logging
import numpy
import pyqtgraph

from PyQt4 import QtCore
from PyQt4 import QtGui

import tables
import vitables
from vitables.vtapp import translate as _translate

from . import _defaults
from .colorrow import ColorRow

class MultiCubeMath(QtGui.QMdiSubWindow):
    """The class to perform cross data set frame math.

    This window does awesomeness with the awesome.  It takes like *two
    or three* cubes and does like **math**!!! OMGROFLOLWTFPDQBACH!!!!
    **I know right!!**

    """

    def __init__(self, parent):
        """Initialize the cube math window.
        
        Parameters
        ----------

        parent : :class:`PyQt4.QtGui.QMdiArea`
            The workspace from ViTables.

        """
        logger = logging.getLogger(__name__ +".MultiCubeMath")
        super(MultiCubeMath, self).__init__(parent)

        indexes = vitables.utils.getSelectedIndexes()
        if len(indexes) > 3:
            msg = "A maximum of 3 leafs may be selected.  Ignoring {:d}"
            logger.warn(_translate(
                _defaults["PLUGIN_CLASS"],
                msg.format(len(indexes) -3),
                "Pluggin warning message"
            ))


        self.red_index = indexes[0]
        if len(indexes) > 1:
            self.green_index = indexes[1]
        else:
            self.green_index = None

        if len(indexes) > 2:
            self.blue_index = indexes[2]
        else:
            self.blue_index = None

        self._update_dbt_leaf()
        self.pindex = None

        widget = QtGui.QWidget(parent)
        self.setWidget(widget)

        self._layout = QtGui.QGridLayout(self.widget())
        self._layout.setMargin(0)
        self._layout.setSpacing(0)

        self.image_view = pyqtgraph.ImageView(parent=self.widget())
        self._layout.addWidget(self.image_view, 0, 0, 1, 1)
        self._layout.setRowStretch(0, 10)

        self._add_color_panels(indexes)
        #self._red = ColorRow(self, index=self.red_index, color="r")
        #self._red.setTitle("R")
        #self._layout.addWidget(self._red, 1, 0, 1, 1)

        #self._green = ColorRow(self, index=self.green_index, color="g")
        #self._green.setTitle("G")
        #self._layout.addWidget(self._green, 2, 0, 1, 1)

        #self._blue = ColorRow(self, index=self.blue_index, color="b")
        #self._blue.setTitle("B")
        #self._layout.addWidget(self._blue, 3, 0, 1, 1)

        #for it in range(1,4):
            #self._layout.setRowStretch(it, 1)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle(_translate(
            _defaults["PLUGIN_CLASS"], "Compare Datasets", "Title"
        ))
        self.setVisible(True)

    def _update_dbt_leaf(self):
        """Have the ``dbt_leaf`` mirror one of the leaves.
        
        This ensures that at least one node is assigned to the leaf.  If
        it were not, we would get obnoxious error when the application
        was closed with subwindow open.  It cycles through three colors
        looking for the first one that is not ``None`` and uses that
        leaf.  If all values are ``None``, it does not change the leaf.

        """
        dbt = vitables.utils.getGui().dbs_tree_model
        for idx in (self.red_index, self.green_index, self.blue_index):
            if idx is not None:
                self.dbt_leaf = dbt.nodeFromIndex(idx)

    def _add_color_panels(self, indexes):
        """Add the color channels to the window.

        Create the channel selector panels and place them at the bottom
        of the window.  The panels are place in a column beneath the
        image view.  The nodes are selected from the provided list of
        indexes in the order of Red, Green, and then Blue.  If the list
        is not long enough to select one of the colors, it is set to the
        the null selection.

        Parameters
        ----------

        indexes : list
            The list of indexes selected in ViTables.

        """
        colors = ("Red", "Green", "Blue")
        self._colors = {}
        for row in range(1, 4):
            color = colors[row -1]
            if len(indexes) >= row:
                index = indexes[row -1]
            else:
                index = None

            self._colors[color] = ColorRow(
                self, index=index, color=color[0].lower()
            )
            self._colors[color].setTitle(color)
            self._layout.addWidget(self._colors[color], row, 0, 1, 1)
            self._layout.setRowStretch(row, 1)


    def _add_math_group(self):
        """Create a panel to hold the math options.

        """
        self._math_group = QtGui.QGroupBox()
        self._math_layout = QtGui.QGridLayout(self._math_group)
        self._math_layout.setMargin(0)
        self._math_layout.setSpacing(0)

        buttons = (
            ("RGB", self._show_rgb),
            ("R - G", self._show_r_minus_g),
            ("R / G", self._show_r_by_g),
            ("(R - G) / B", self._show_r_minus_g_by_b),
        )
        row = -1
        self._math_buttons = QtGui.QButtonGroup(self._math_group)
        for  label, function in buttons:
            row += 1
            button = QtGui.QRadioButton(label, self._math_group)
            self._math_buttons.addButton(button)
            button.clicked.connect(function)
            self._math_layout.addWidget(button, row, 0, 1, 1)

        self._layout.addWidget(

        )


