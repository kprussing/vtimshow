#!/usr/bin/env python3
__doc__="""The default do nothing filter.

This filter does nothing to the array and simply returns ``None``.  This
is to be used for the default selection in the :class:`Filters`
selection.

"""
from vitables.vtapp import translate as _translate

from .. import plugin_class

name = "No filter"
"""The filter name."""

def compute(array):
    """Process the array.

    This routine simply returns ``None`` if it was passed a
    :class:`numpy.ndarray` that has ``ndim == 3``.  Otherwise, it raises
    a ``RuntimeError``.

    Parameters
    ----------

    array : :class:`numpy.ndarray`
        The array to check the dimensions.

    Returns
    -------

    ``None``

    Raises
    ------

    RuntimeError
        If the array is not 3 dimensions.

    """
    if array.ndim != 3:
        raise RuntimeError(_translate(
            plugin_class,
            "Invalid array with dimension {0:d}".format(array.ndim),
            "Plugin error message"
        ))

    return None

