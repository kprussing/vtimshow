#!/usr/bin/env python3
__doc__="""The module defining a dialog to reshape the image."""

import collections
import logging
import os
import pkg_resources
import numpy

from PyQt4 import QtGui
from PyQt4 import uic

Dimension = collections.namedtuple(
    "Dimension", ["dim", "start", "end", "stride"]
)
"""Convenience class for organizing dimensions."""

class SetDims(QtGui.QDialog):
    """A dialog to reshape the image.

    This class provides a means to transpose the array used as an image
    once it has been loaded into memory.  The default orientation
    specified by the :class:`preferences.Preferences` can be set for the
    most common orientation encountered; however, we are not guaranteed
    to get every dataset with that orientation.  This provides a means
    to dynamically reshape the image.  By default, the height and width
    are taken as the first two dimensions.  The third dimension defaults
    to the depth.  If the given array has three or four dimensions, the
    RGB(A) combo box is activated and all dimensions that are 3 or 4 in
    size are added a valid options.

    """

    def __init__(self, array, parent=None):
        """
        Get the dimension assignments from the user.

        Given a :class:`numpy.ndarray` compatible array, let the user
        decide which dimensions are the width, height, depth, and
        possibly RGB(A).  The given array must have a ``shape``
        attribute analogous to the :class:`numpy.ndarray` attribute.

        Parameters
        ----------

        array : array_like
            :class:`numpy.ndarray` compatible objects with a ``shape``
            attribute.
        parent : :class:`PyQt4.QtGui.QWidget`, optional
            The parent widget.

        """
        super(SetDims, self).__init__(parent)
        uic.loadUi(
            pkg_resources.resource_filename(__name__, "setdims.ui"),
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
            self.depthComboBox.addItem("None")
            self._set_combobox(self.depthComboBox)
            self.depthComboBox.setCurrentIndex(1)
            self.depthComboBox.currentIndexChanged.connect(
                self._update_depth
            )
            self._update_depth()
            # Assume the first dimension is the depth.  That means the
            # width and height need to be shifted back one.
            self.heightComboBox.setCurrentIndex(1)
            self.widthComboBox.setCurrentIndex(2)

        self._set_rgbaComboBox()
        self.show()

    def _set_combobox(self, combobox):
        """Add the values to the combo box.

        Parameters
        ----------

        combobox : QComboBox
            The box to which to add the values in ``self.dims``

        """
        for it in range(len(self.dims)):
            combobox.addItem("dim{0:d}".format(it))

        return

    def _set_rgbaComboBox(self):
        """Add dimensions of size 3 or 4 to RGB(A) combo box"""
        self.rgbaComboBox.setEnabled(False)
        if len(self.dims) < 3:
            return

        self.rgbaComboBox.addItem("None")
        fmt = "dim{0:d} ({1:s})"
        for it in range(len(self.dims)):
            if self.dims[it] == 3:
                item = fmt.format(it, "RGB")
            elif self.dims[it] == 4:
                item = fmt.format(it, "RGBA")
            else:
                continue

            self.rgbaComboBox.addItem(item)

        if self.rgbaComboBox.count() > 1:
            self.rgbaComboBox.setEnabled(True)

    def _combobox_text_to_index(self, combobox):
        """Parse the text of the combo box for the proper index.

        The proper index is taken from the string in the combo box.

        Parameters
        ----------

        combobox : QComboBox
            The box from which to extract the index

        """
        if combobox.isEnabled():
            text = combobox.currentText()
            if text == "None":
                return None
            else:
                return int(text.split()[0][3:])
        else:
            return None


    def _update_height(self):
        """Update the height boxes."""
        idx = self._combobox_text_to_index(self.heightComboBox)
        if idx is None:
            return

        maxval = self.dims[idx]
        self.heightSpinBoxStart.setRange(0, maxval)
        self.heightSpinBoxStart.setValue(0)
        self.heightSpinBoxEnd.setRange(0, maxval)
        self.heightSpinBoxEnd.setValue(maxval)
        self.heightSpinBoxStride.setRange(0, maxval)
        self.heightMaxLabel.setText("{0:d}".format(maxval))
        return

    def _update_width(self):
        """Update the width boxes."""
        idx = self._combobox_text_to_index(self.widthComboBox)
        if idx is None:
            return

        maxval = self.dims[idx]
        self.widthSpinBoxStart.setRange(0, maxval)
        self.widthSpinBoxStart.setValue(0)
        self.widthSpinBoxEnd.setRange(0, maxval)
        self.widthSpinBoxEnd.setValue(maxval)
        self.widthSpinBoxStride.setRange(0, maxval)
        self.widthMaxLabel.setText("{0:d}".format(maxval))
        return

    def _update_depth(self):
        """Update the depth boxes."""
        idx = self._combobox_text_to_index(self.depthComboBox)
        if idx is None:
            self.depthSpinBoxStart.setValue(0)
            self.depthSpinBoxStart.setEnabled(False)
            self.depthSpinBoxEnd.setValue(0)
            self.depthSpinBoxEnd.setEnabled(False)
            self.depthSpinBoxStride.setValue(1)
            self.depthSpinBoxStride.setEnabled(False)
            self.depthMaxLabel.setText("")
            return

        maxval = self.dims[idx]
        self.depthSpinBoxStart.setRange(0, maxval)
        self.depthSpinBoxStart.setValue(0)
        self.depthSpinBoxStart.setEnabled(True)
        self.depthSpinBoxEnd.setRange(0, maxval)
        self.depthSpinBoxEnd.setValue(maxval)
        self.depthSpinBoxEnd.setEnabled(True)
        self.depthSpinBoxStride.setRange(1, maxval-1)
        self.depthSpinBoxStride.setValue(1)
        self.depthSpinBoxStride.setEnabled(True)
        self.depthMaxLabel.setText("{0:d}".format(maxval))
        return

    def get_height(self):
        """Return the height dimensions."""
        if not self.heightComboBox.isEnabled():
            return None

        idx = self._combobox_text_to_index(self.heightComboBox)
        if idx is None:
            return None

        return Dimension(
            dim=idx,
            start=self.heightSpinBoxStart.value(),
            end=self.heightSpinBoxEnd.value(),
            stride=self.heightSpinBoxStride.value()
        )

    def get_width(self):
        """Return the width dimensions."""
        if not self.widthComboBox.isEnabled():
            return None
        idx = self._combobox_text_to_index(self.widthComboBox)
        if idx is None:
            return None

        return Dimension(
            dim=idx,
            start=self.widthSpinBoxStart.value(),
            end=self.widthSpinBoxEnd.value(),
            stride=self.widthSpinBoxStride.value()
        )

    def get_depth(self):
        """Return the depth dimensions."""
        if not self.depthComboBox.isEnabled():
            return None

        idx = self._combobox_text_to_index(self.depthComboBox)
        if idx is None:
            return None

        return Dimension(
            dim=idx,
            start=self.depthSpinBoxStart.value(),
            end=self.depthSpinBoxEnd.value(),
            stride=self.depthSpinBoxStride.value()
        )

    def get_rgba(self):
        """Return the RGB(A) dimension."""
        if not self.rgbaComboBox.isEnabled():
            return None

        idx = self._combobox_text_to_index(self.rgbaComboBox)
        if idx is None:
            return None

        return Dimension(dim=idx, start=None, end=None, stride=None)

def _main():
    """Test the dialog."""
    import numpy
    import sys
    logging.basicConfig(level=logging.DEBUG)
    app = QtGui.QApplication(sys.argv)
    array = numpy.random.random((3,256,320,63))
    ex = SetDims(array)
    if ex.exec():
        print("Width : {0!s}".format(ex.get_width()))
        print("Height: {0!s}".format(ex.get_height()))
        print("Depth : {0!s}".format(ex.get_depth()))
        print("RGBA  : {0!s}".format(ex.get_rgba()))
        ex.close()

    sys.exit(app.exec_())

if __name__ == "__main__":
    _main()

