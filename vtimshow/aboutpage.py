#!/usr/bin/env python3
__doc__="""The module defining the about page."""
import logging
import os

from PyQt4 import QtGui
from PyQt4 import uic

from .preferences import Preferences

class AboutPage(QtGui.QWidget):
    """The about page loaded by ViTables in the preferences window.

    This is the module that is required by ViTables for the preferences
    window.  It follows the format used by the CSV tools distributed
    with ViTables and includes the module version, name, folder, author,
    and comment.  It adds combo boxes to allow the user to define the
    preferred orientation of the data sets in the files.  By default,
    the arrays are assumed to be row-major order.  This places the index
    of the time series as the first index of a 3D or 4D array.

    """

    def __init__(self, desc, parent=None):
        """Initialize the about page.

        The 'version', 'module_name', 'folder', 'author', and 'comment'
        are extracted from the dictionary ``desc`` and stored as the
        appropriate member variables.

        Parameters
        ----------

        desc : dict
            The description dictionary.
        parent : QWidget, optional
            The parent widget.

        """
        logger = logging.getLogger(__name__ +".AboutPage")
        super(AboutPage, self).__init__(parent)
        logger.debug("Load the UI")
        uic.loadUi(
            os.path.join(os.path.dirname(__file__), "aboutpage.ui"),
            self
        )

        # Set the default information.
        self.version_le.setText(desc['version'])
        self.module_name_le.setText(desc['module_name'])
        self.folder_le.setText(desc['folder'])
        self.author_le.setText(desc['author'])
        self.desc_te.setText(desc['comment'])

        ## Get the data file.
        logger.debug("Read the preference file")
        self.config = Preferences()

        self.height_2d.setCurrentIndex(int(self.config["2D"]["Height"]))
        self.width_2d.setCurrentIndex(int(self.config["2D"]["Width"]))
        self.rgba_2d.setCurrentIndex(int(self.config["2D"]["RGB(A)"]))

        self.height_3d.setCurrentIndex(int(self.config["3D"]["Height"]))
        self.width_3d.setCurrentIndex(int(self.config["3D"]["Width"]))
        self.depth_3d.setCurrentIndex(int(self.config["3D"]["Depth"]))

        self.height_4d.setCurrentIndex(int(self.config["4D"]["Height"]))
        self.width_4d.setCurrentIndex(int(self.config["4D"]["Width"]))
        self.depth_4d.setCurrentIndex(int(self.config["4D"]["Depth"]))
        self.rgba_4d.setCurrentIndex(int(self.config["4D"]["RGB(A)"]))

        self.height_2d.currentIndexChanged.connect(self.update_config)
        self.width_2d.currentIndexChanged.connect(self.update_config)
        self.rgba_2d.currentIndexChanged.connect(self.update_config)

        self.height_3d.currentIndexChanged.connect(self.update_config)
        self.width_3d.currentIndexChanged.connect(self.update_config)
        self.depth_3d.currentIndexChanged.connect(self.update_config)

        self.height_4d.currentIndexChanged.connect(self.update_config)
        self.width_4d.currentIndexChanged.connect(self.update_config)
        self.depth_4d.currentIndexChanged.connect(self.update_config)
        self.rgba_4d.currentIndexChanged.connect(self.update_config)

        self.saveButton.clicked.connect(self.save)

    def update_config(self):
        """Update the preferences configuration structure."""
        self.config["2D"]["Height"] = self.height_2d.currentText()
        self.config["2D"]["Width"] = self.width_2d.currentText()
        self.config["2D"]["RGB(A)"] = self.rgba_2d.currentText()

        self.config["3D"]["Height"] = self.height_3d.currentText()
        self.config["3D"]["Width"] = self.width_3d.currentText()
        self.config["3D"]["Depth"] = self.depth_3d.currentText()

        self.config["4D"]["Height"] = self.height_4d.currentText()
        self.config["4D"]["Width"] = self.width_4d.currentText()
        self.config["4D"]["Depth"] = self.depth_4d.currentText()
        self.config["4D"]["RGB(A)"] = self.rgba_4d.currentText()

    def save(self):
        """Write the configuration to file."""
        logger = logging.getLogger(__name__ +".AboutPage.save")
        logger.debug("Dump to file {0:s}".format(self.config.inifile))
        with open(self.config.inifile, "w") as fid:
            self.config.write(fid)

