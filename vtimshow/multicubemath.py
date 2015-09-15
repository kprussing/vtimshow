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

from . import plugin_class
from .colorrow import ColorRow
from .utils import divide

class MultiCubeMath(QtGui.QMdiSubWindow):
    """The class to perform cross data set frame math.

    This class defines the window that can compare multiple datasets.
    The main portion of the window is a :class:`pyqtgraph.ImageView`
    that displays the resultant image.  The user assigns each color to a
    dataset that has been revealed in the tree viewer and then selects
    the mathematical operation to perform on the datasets.  If the user
    selects datasets that cannot be used in a valid equation, the
    corresponding buttons are disabled.

    ..  note::  The ability to work with 4D arrays is included; however,
                this functionality is considered experimental because a
                set of 4D test data sets is not currently available.

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
                plugin_class,
                msg.format(len(indexes) -3),
                "Pluggin warning message"
            ))


        widget = QtGui.QWidget(parent)
        self.setWidget(widget)

        self._layout = QtGui.QGridLayout(self.widget())
        self._layout.setMargin(0)
        self._layout.setSpacing(0)

        self.image_view = pyqtgraph.ImageView(parent=self.widget())
        self._layout.addWidget(self.image_view, 0, 0, 1, 1)
        self._layout.setRowStretch(0, 10)
        self._layout.setColumnStretch(0, 10)

        self._add_color_panels(indexes)
        self._add_math_group()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle(_translate(
            plugin_class, "Compare Datasets", "Title"
        ))
        self.setVisible(True)

        self._update_dbt_leaf()
        self.pindex = None

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
            self._colors[color].frame_changed.connect(
                self._update_image
            )

    def _add_math_group(self):
        """Create a panel to hold the math options."""
        self._math_group = QtGui.QGroupBox()
        self._math_layout = QtGui.QGridLayout(self._math_group)
        self._math_layout.setMargin(0)
        self._math_layout.setSpacing(0)

        buttons = (
            ("R", self._show_r),
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

        self._layout.addWidget(self._math_group, 1, 1, 3, 1)
        self._update_math_group()

    def _get_frames(self):
        """Programmatically get the frames."""
        R = self._colors["Red"].get_frame()
        G = self._colors["Green"].get_frame()
        B = self._colors["Blue"].get_frame()
        return R, G, B

    def _show_r(self):
        """Show the R band image in monochrome."""
        R, G, B = self._get_frames()
        #self.image_view.getImageItem().updateImage(R)
        # Calling ``updateImage`` also works, but the brightness range
        # is not automatically updated.  So, just set the image for now.
        self.image_view.setImage(R)

    def _show_rgb(self):
        """Show the RGB image."""
        R, G, B = self._get_frames()
        image = numpy.dstack((R, G, B))
        self.image_view.setImage(image)

    def _show_r_minus_g(self):
        """Show :math:`R - G`."""
        R, G, B = self._get_frames()
        self.image_view.setImage(R - G)

    def _show_r_by_g(self):
        """Show :math:`R / G`."""
        R, G, B = self._get_frames()
        self.image_view.setImage(divide(R, G))

    def _show_r_minus_g_by_b(self):
        """Show :math:`(R - G) / B`."""
        R, G, B = self._get_frames()
        self.image_view.setImage(divide(R - G, B))

    def _update_dbt_leaf(self):
        """Have the ``dbt_leaf`` mirror one of the leaves.

        This ensures that at least one node is assigned to the leaf.  If
        it were not, we would get an obnoxious error when the
        application was closed with subwindow open.  It cycles through
        the three colors looking for the first one that is not ``None``
        and uses that leaf.  If all values are ``None``, it does not
        change the leaf.

        """
        databases = vitables.utils.getGui().dbs_tree_model
        for color in self._colors.values():
            if color.index is not None:
                self.dbt_leaf = databases.nodeFromIndex(color.index)
                break

    def _update_image(self):
        """Call all update routines after updating the image."""
        self._update_math_group()
        button = self._math_buttons.checkedButton()
        if button is not None and button.isEnabled():
            button.click()


    def _update_math_group(self):
        """Ensure only reasonable math can be performed.

        When a leaf node has been changed, we need to make sure only
        rational math can be performed.  If a particular color has been
        set to the null value, we disable any math that uses that color.
        After that check, we take the red channel as the standard and
        make sure that we can generate a sane image.  For example, it
        makes no sense to use 4D images with RGB.  Also, we must be able
        to broadcast the images together to perform the math.

        """
        for button in self._math_buttons.buttons():
            button.setEnabled(True)

        if self._colors["Red"].index is None:
            for button in self._math_buttons.buttons():
                button.setEnabled(False)

            return

        for key in ("Green", "Blue"):
            if self._colors[key].index is None:
                for button in self._math_buttons.buttons():
                    if key[0] in button.text():
                        button.setEnabled(False)

        rgb = False
        compatible = True
        dims = self._colors["Red"].data.shape
        for key, val in self._colors.items():
            if key == "Red" or val.index is None:
                continue

            rgb |= (val.data.ndim == 4) | (
                (val.data.ndim == 3) & val.node_is_2d()
            )
            for d1, d2 in zip(dims[::-1], val.data.shape[::-1]):
                compatible &= (d1 == 1) | (d2 == 1) | (d1 == d2)

        for button in self._math_buttons.buttons():
            if not button.isEnabled() or button.text() == "R":
                # Skip any button that has already been flagged as
                # invalid, and let the 'R' button stay active because we
                # know the red channel is populated.
                continue

            if button.text() == "RGB":
                button.setEnabled(not rgb)
            else:
                button.setEnabled(compatible)

