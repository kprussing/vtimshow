#!/usr/bin/env python3
__doc__="""The module defining an order preferences class."""

import configparser
import os
import pkg_resources

class Preferences(configparser.ConfigParser):
    """A class to handle the order preferences.

    This holds the details regarding the preferred order of the
    dimensions for 2D, 3D, and 4D arrays.  Because this class inherits
    from :class:`configparser.ConfigParser`, we simply add the sections
    '2D', '3D', and '4D' to the parser to define the three possible
    scenarios.  The options in each section are 'Depth', 'Height',
    'Width', and 'RGB(A)' as appropriate.  Reading and writing the
    preferences file is left to the base class; however, if the INI file
    is not provided on construction, a row-major ordering is assumed.

    >>> pref = Preferences()
    >>> for dim in ('Height', 'Width', 'RGB(A)'):
    ...     print(dim, pref['2D'][dim])
    Height 0
    Width 1
    RGB(A) 2
    >>> for dim in ('Depth', 'Height', 'Width'):
    ...     print(dim, pref['3D'][dim])
    Depth 0
    Height 1
    Width 2
    >>> for dim in ('Depth', 'Height', 'Width', 'RGB(A)'):
    ...     print(dim, pref['2D'][dim])
    Depth 0
    Height 1
    Width 2
    RGB(A) 3

    """
    _inifile = pkg_resources.resource_filename(
            __name__, "preferences.ini"
        )

    def __init__(self, inifile=None):
        """Initialize to the given file or use the defaults.

        Parameters
        ----------

        inifile : string, optional
            The path to the INI file to store/read the preferences.

        """
        super(Preferences, self).__init__()
        if inifile is not None:
            self.inifile = inifile
        else:
            self.inifile = self._inifile

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

