#!/usr/bin/env python3
__doc__="""A unified framework to add filters to :class:`ColorRow`.

The primary item defined in this package is :class:`Filters` which is
simply an extension of :class:`PyQt4.QtGui.QComboBox` that adds support
for loading user defined filters along with those distributed with this
package.  The default filters provided are a “Null” filter that does
nothing and filters based on the red, green, and blue response of the 
human eye.

"""

from .filters import Filters

