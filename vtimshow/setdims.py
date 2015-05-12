#!/usr/bin/env python3
import collections
import logging
import os
import numpy

from PyQt4 import QtGui
from PyQt4 import uic

Dimension = collections.namedtuple(
    "Dimension", ["dim", "start", "end", "stride"]
)

class SetDims(QtGui.QDialog):

    def __init__(self, array, parent=None):
        """
        Get the dimension assignments from the user.

        Given a ``numpy`.ndarray` compatible array, let the user decide
        which dimensions are the width, height, and depth.  The given
        ``array`` must have a ``shape`` attribute analogous to the
        ``numpy.ndarray`` attribute.

        Parameters
        ----------

        array : array_like
            ``numpy.ndarray`` compatible objects with a ``shape``
            attribute.
        parent : QWidget, optional
            The parent widget.

        """
        super(SetDims, self).__init__(parent)
        uic.loadUi(
            os.path.join(os.path.dirname(__file__), "setdims.ui"), 
            self
        )
        self.dims = array.shape

        self._set_combobox(self.heightComboBox)
        self.heightComboBox.setCurrentIndex(0)
        self.heightComboBox.currentIndexChanged.connect(
            self._update_height
        )
        self._update_height()

        if len(self.dims) <= 1:
            self.widthComboBox.setEnabled(False)
            self.widthSpinBoxStart.setEnabled(False)
            self.widthSpinBoxEnd.setEnabled(False)
            self.widthSpinBoxStride.setEnabled(False)
        else:
            self._set_combobox(self.widthComboBox)
            self.widthComboBox.setCurrentIndex(1)
            self.widthComboBox.currentIndexChanged.connect(
                self._update_width
            )
            self._update_width()

        if len(self.dims) <= 2:
            self.depthComboBox.setEnabled(False)
            self.depthSpinBoxStart.setEnabled(False)
            self.depthSpinBoxEnd.setEnabled(False)
            self.depthSpinBoxStride.setEnabled(False)
        else:
            self._set_combobox(self.depthComboBox)
            self.depthComboBox.setCurrentIndex(2)
            self.depthComboBox.currentIndexChanged.connect(
                self._update_depth
            )
            self._update_depth()

        self.show()

    def _set_combobox(self, combobox):
        """
        Add the values to the combo box.
        """
        for it in range(len(self.dims)):
            combobox.addItem("dim{0:d}".format(it))

        return

    def _update_height(self):
        """
        Update the height boxes
        """
        maxval = self.dims[self.heightComboBox.currentIndex()]
        self.heightSpinBoxStart.setRange(0, maxval)
        self.heightSpinBoxStart.setValue(0)
        self.heightSpinBoxEnd.setRange(0, maxval)
        self.heightSpinBoxEnd.setValue(maxval)
        self.heightSpinBoxStride.setRange(0, maxval)
        self.heightMaxLabel.setText("{0:d}".format(maxval))
        return

    def _update_width(self):
        """
        Update the width boxes
        """
        maxval = self.dims[self.widthComboBox.currentIndex()]
        self.widthSpinBoxStart.setRange(0, maxval)
        self.widthSpinBoxStart.setValue(0)
        self.widthSpinBoxEnd.setRange(0, maxval)
        self.widthSpinBoxEnd.setValue(maxval)
        self.widthSpinBoxStride.setRange(0, maxval)
        self.widthMaxLabel.setText("{0:d}".format(maxval))
        return

    def _update_depth(self):
        """
        Update the depth boxes
        """
        maxval = self.dims[self.depthComboBox.currentIndex()]
        self.depthSpinBoxStart.setRange(0, maxval)
        self.depthSpinBoxStart.setValue(0)
        self.depthSpinBoxEnd.setRange(0, maxval)
        self.depthSpinBoxEnd.setValue(maxval)
        self.depthSpinBoxStride.setRange(0, maxval)
        self.depthMaxLabel.setText("{0:d}".format(maxval))
        return

    def get_height(self):
        """
        Return the height dimensions
        """
        if not self.heightComboBox.isEnabled():
            return None

        return Dimension(
            dim=self.heightComboBox.currentIndex(),
            start=self.heightSpinBoxStart.value(),
            end=self.heightSpinBoxEnd.value(),
            stride=self.heightSpinBoxStride.value()
        )

    def get_width(self):
        """
        Return the width dimensions
        """
        if not self.widthComboBox.isEnabled():
            return None

        return Dimension(
            dim=self.widthComboBox.currentIndex(),
            start=self.widthSpinBoxStart.value(),
            end=self.widthSpinBoxEnd.value(),
            stride=self.widthSpinBoxStride.value()
        )

    def get_depth(self):
        """
        Return the depth dimensions
        """
        if not self.depthComboBox.isEnabled():
            return None

        return Dimension(
            dim=self.depthComboBox.currentIndex(),
            start=self.depthSpinBoxStart.value(),
            end=self.depthSpinBoxEnd.value(),
            stride=self.depthSpinBoxStride.value()
        )

def main():
    """
    Test the dialog.
    """
    import numpy
    import sys
    logging.basicConfig(level=logging.DEBUG)
    app = QtGui.QApplication(sys.argv)
    array = numpy.random.random((256,320,63))
    ex = SetDims(array)
    if ex.exec():
        print(ex.get_width())
        print(ex.get_height())
        print(ex.get_depth())
        ex.close()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

