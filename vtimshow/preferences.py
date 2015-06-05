#!/usr/bin/env python3
import configparser
import os

class Preferences(configparser.ConfigParser):
    """
    A class to handle the preferences.

    This holds the details regarding the preferred order of the
    dimensions for 2D, 3D, and 4D arrays.  
    """
    inifile = os.path.join(os.path.dirname(__file__), "preferences.ini")

    def __init__(self, inifile=None):
        super(Preferences, self).__init__()
        if inifile is not None:
            self.inifile = inifile

        self.read(self.inifile)
        for dim in ("2D", "3D", "4D"):
            if dim not in self:
                self[dim] = {}

            opts = ("Depth", "Height", "Width", "RGB(A)")
            for opt in opts:
                if dim == "2D":
                    if opt == "Depth":
                        continue
                    else:
                        val = str(opts.index(opt) -1)

                elif dim == "3D" and opt == "RGB(A)":
                    continue

                else:
                    val = str(opts.index(opt))

                if opt not in self[dim]:
                    self[dim][opt] = val

