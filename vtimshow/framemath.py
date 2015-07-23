#!/usr/bin/env python3
__doc__="""The module defining :class:`FrameMath`."""

import logging
import numpy
import pyqtgraph

from PyQt4 import QtCore
from PyQt4 import QtGui

import vitables
from vitables.vtapp import translate as _translate

from . import _defaults
from .utils import divide as _divide

class FrameMath:
    """The class to hold the parameters for frame math.

    This class takes a reference to the parent :class:`ImageWindow`.  It
    then adds a frame to the bottom of the :class:`pyqtgraph.ImageView`
    embedded in the parent.  By default, this frame is hidden and a menu
    option option to toggle visibility is added to the menu button in
    the window.  When the frame is toggled on, the default frame
    selector is toggled off.  Instead, color coded selector for R, G,
    and B frames are added to the time series plot.  These may be
    dragged along the axis or set with the connected spin boxes.  The
    bottom of the frame ha radio buttons that will perform simple
    arithmetic on the frames and display the monochrome results, or it
    will display the RGB combination of the bands.

    """
    R = None
    G = None
    B = None

    def __init__(self, parent):
        """Initialize the math frame.

        Parameters
        ----------

        parent : :class:`pyqtgraph.ImageView`
            The parent widget holding the image

        """
        logger = logging.getLogger(__name__ +".FrameMath")
        #imageItem = parent.image.getImageItem()
        self.parent = parent

        image = parent.image.image
        if len(image.shape) != 3 or image.shape[0] < 2:
            return

        self.group = QtGui.QGroupBox()
        self.layout = QtGui.QGridLayout(self.group)
        self.layout.setMargin(0)
        self.layout.setSpacing(0)

        label_1 = QtGui.QLabel(self.group)
        label_1.setText(
            _translate(
                _defaults["PLUGIN_CLASS"], "Select Frames:", "Label"
            )
        )

        # Mimic the normalization panel.
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        label_1.setFont(font)
        self.layout.addWidget(label_1, 0, 0, 1, 1)

        label_2 = QtGui.QLabel(self.group)
        label_2.setText("R")
        label_2.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
        )
        self.layout.addWidget(label_2, 0, 1, 1, 1)

        # Add math radio buttons.
        self.buttons = QtGui.QButtonGroup(self.group)

        button = QtGui.QRadioButton("RGB", self.group)
        self.buttons.addButton(button)
        button.clicked.connect(self._show_rgb)
        self.layout.addWidget(button, 1, 1, 1, 1)

        button = QtGui.QRadioButton("R - G", self.group)
        self.buttons.addButton(button)
        button.clicked.connect(self._show_r_minus_g)
        self.layout.addWidget(button, 1, 2, 1, 1)

        button = QtGui.QRadioButton("R / G", self.group)
        self.buttons.addButton(button)
        button.clicked.connect(self._show_r_by_g)
        self.layout.addWidget(button, 1, 3, 1, 1)

        button = QtGui.QRadioButton("(R - G) / B", self.group)
        self.buttons.addButton(button)
        button.clicked.connect(self._show_r_minus_g_by_b)
        self.layout.addWidget(button, 1, 4, 1, 1)

        # Add the Red channel
        self.rSpin = QtGui.QSpinBox(self.group)
        self.rSpin.setRange(0, image.shape[0])
        self.layout.addWidget(self.rSpin, 0, 2, 1, 1)

        self.rLine = pyqtgraph.InfiniteLine(movable=True, pen="r")
        self.parent.image.ui.roiPlot.addItem(self.rLine)
        self.rLine.setVisible(False)

        self.rLine.sigPositionChanged.connect(self._r_line_changed)
        self.rSpin.valueChanged.connect(self._r_spin_changed)
        self.rSpin.setValue(0)

        # Add the Green channel
        label_3 = QtGui.QLabel(self.group)
        label_3.setText("G")
        label_3.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
        )
        self.layout.addWidget(label_3, 0, 3, 1, 1)
        self.gSpin = QtGui.QSpinBox(self.group)
        self.gSpin.setRange(0, image.shape[0])
        self.layout.addWidget(self.gSpin, 0, 4, 1, 1)

        self.gLine = pyqtgraph.InfiniteLine(movable=True, pen="g")
        self.parent.image.ui.roiPlot.addItem(self.gLine)
        self.gLine.setVisible(False)

        self.gLine.sigPositionChanged.connect(self._g_line_changed)
        self.gSpin.valueChanged.connect(self._g_spin_changed)
        self.gSpin.setValue(1)

        # Add the Blue channel
        label_4 = QtGui.QLabel(self.group)
        label_4.setText("B")
        label_4. setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
        )
        self.layout.addWidget(label_4, 0, 5, 1, 1)
        self.bSpin = QtGui.QSpinBox(self.group)
        self.bSpin.setRange(0, image.shape[0])
        self.layout.addWidget(self.bSpin, 0, 6, 1, 1)

        self.bLine = pyqtgraph.InfiniteLine(movable=True, pen="b")
        self.parent.image.ui.roiPlot.addItem(self.bLine)
        self.bLine.setVisible(False)

        self.bLine.sigPositionChanged.connect(self._b_line_changed)
        self.bSpin.valueChanged.connect(self._b_spin_changed)
        self.bSpin.setValue(min(2, image.shape[0]))

        # Add the group to the bottom of the third grid layout in the
        # image view.
        self.parent.image.ui.gridLayout_3.addWidget(
            self.group, 2, 0, 1, 1
        )

        self.group.setTitle(
            _translate(
                _defaults["PLUGIN_CLASS"], "Frame math", "Layout"
            )
        )
        self.group.hide()

        # Add to the parent image view menu.
        self.menuAction = QtGui.QAction(
            "Frame math", self.parent.image.menu
        )
        self.menuAction.setCheckable(True)
        self.menuAction.toggled.connect(self.toggled)
        self.parent.image.menu.addAction(self.menuAction)

    def _r_line_changed(self):
        """Update the R spin box and image."""
        self.rSpin.setValue(self.rLine.value())
        self._update_image()

    def _r_spin_changed(self):
        """Update the R line."""
        self.rLine.setValue(self.rSpin.value())

    def _g_line_changed(self):
        """Update the G spin box and image."""
        self.gSpin.setValue(self.gLine.value())
        self._update_image()

    def _g_spin_changed(self):
        """Update the G line."""
        self.gLine.setValue(self.gSpin.value())

    def _b_line_changed(self):
        """Update the B spin box and image."""
        self.bSpin.setValue(self.bLine.value())
        self._update_image()

    def _b_spin_changed(self):
        """Update the B line."""
        self.bLine.setValue(self.bSpin.value())

    def toggled(self, b):
        """Toggle the frame on and off.

        Toggle the R, G, and B selectors to be visible when the frame is
        and the default frame selector to be the opposite.

        Parameters
        ----------

        b : bool
            Passed by the menu signal.

        """
        self.group.setVisible(b)

        for line in (self.rLine, self.gLine, self.bLine):
            line.setVisible(b)

        self.parent.image.timeLine.setVisible(not b)

    def _rgb_frames(self):
        """Programmatically get the frames."""
        image = self.parent.image.image
        R = image[self.rSpin.value(), :, :]
        G = image[self.gSpin.value(), :, :]
        B = image[self.bSpin.value(), :, :]
        return R, G, B

    def _show_rgb(self):
        """Show the RGB image."""
        R, G, B = self._rgb_frames()
        image = numpy.dstack((R, G, B))
        imageItem = self.parent.image.getImageItem()
        imageItem.updateImage(image)

    def _show_r_minus_g(self):
        """Compute and show :math:`R - G`."""
        R, G, B = self._rgb_frames()
        image = R - G
        imageItem = self.parent.image.getImageItem()
        imageItem.updateImage(image)

    def _show_r_minus_g_by_b(self):
        """Compute and show :math:`(R - G) / B`."""
        R, G, B = self._rgb_frames()
        image = _divide((R - G), B)
        imageItem = self.parent.image.getImageItem()
        imageItem.updateImage(image)

    def _show_r_by_g(self):
        """Compute and show :math:`R / G`."""
        R, G, B = self._rgb_frames()
        image = _divide(R, G)
        imageItem = self.parent.image.getImageItem()
        imageItem.updateImage(image)

    def _update_image(self):
        """Determine which button is pressed and refresh the image."""
        button = self.buttons.checkedButton()
        if button is None:
            return

        button.click()

