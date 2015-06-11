
import logging
import numpy
import pyqtgraph

from PyQt4 import QtCore
from PyQt4 import QtGui

import vitables
from vitables.vtapp import translate

from . import _defaults

class FrameMath:
    """
    The class to hold the parameters for frame math.

    This class takes a reference to parent image window and the general
    parent used to initialize the norm interface in the ImageView owned
    by the parent.  The initializer adds the frame, adds a new menu
    option, and connects all of the signals.  The class also keeps a
    reference to the R, G, and B frames in the image stack
    """
    R = None
    G = None
    B = None

    def __init__(self, parent, Form=None):
        """
        """
        logger = logging.getLogger(__name__ +".FrameMath")
        #imageItem = parent.image.getImageItem()
        self.parent = parent

        image = parent.image.image
        if len(image.shape) != 3 or image.shape[0] < 2:
            return

        self.group = QtGui.QGroupBox(Form)
        self.layout = QtGui.QGridLayout(self.group)
        self.layout.setMargin(0)
        self.layout.setSpacing(0)

        label_1 = QtGui.QLabel(self.group)
        label_1.setText(
            translate(
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
            translate(_defaults["PLUGIN_CLASS"], "Frame math", "Layout")
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
        self.rSpin.setValue(self.rLine.value())
        self._update_image()

    def _r_spin_changed(self):
        self.rLine.setValue(self.rSpin.value())

    def _g_line_changed(self):
        self.gSpin.setValue(self.gLine.value())
        self._update_image()

    def _g_spin_changed(self):
        self.gLine.setValue(self.gSpin.value())

    def _b_line_changed(self):
        self.bSpin.setValue(self.bLine.value())
        self._update_image()

    def _b_spin_changed(self):
        self.bLine.setValue(self.bSpin.value())

    def toggled(self, b):
        self.group.setVisible(b)

        for line in (self.rLine, self.gLine, self.bLine):
            line.setVisible(b)

        self.parent.image.timeLine.setVisible(not b)

    def _rgb_frames(self):
        image = self.parent.image.image
        R = image[self.rSpin.value(), :, :]
        G = image[self.gSpin.value(), :, :]
        B = image[self.bSpin.value(), :, :]
        return R, G, B

    def _show_rgb(self):
        R, G, B = self._rgb_frames()
        image = numpy.dstack((R, G, B))
        imageItem = self.parent.image.getImageItem()
        imageItem.updateImage(image)

    def _show_r_minus_g(self):
        R, G, B = self._rgb_frames()
        image = R - G
        imageItem = self.parent.image.getImageItem()
        imageItem.updateImage(image)

    def _show_r_minus_g_by_b(self):
        R, G, B = self._rgb_frames()
        image = self._divide((R - G), B)
        imageItem = self.parent.image.getImageItem()
        imageItem.updateImage(image)

    def _show_r_by_g(self):
        R, G, B = self._rgb_frames()
        image = self._divide(R, G)
        imageItem = self.parent.image.getImageItem()
        imageItem.updateImage(image)

    def _divide(self, A, B):
        """
        Compute A / B element wise.

        Given two NumPy arrays, perform the element wise division.
        Replace all NaNs, Infs, and places where B == 0 with 0.
        """
        with numpy.errstate(invalid="ignore", divide="ignore"):
            res = A / B

        res[numpy.isclose(B, 0)] = 0
        res[numpy.isnan(res)] = 0
        res[numpy.isinf(res)] = 0
        return res

    def _update_image(self):
        """
        Determine which button is pressed and refresh the image.
        """
        button = self.buttons.checkedButton()
        if button is None:
            return

        button.click()

