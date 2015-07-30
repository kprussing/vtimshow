#!/usr/bin/env python3
__doc__="""The module to define the filter class."""
import logging
import pkg_resources

from PyQt4 import QtGui

from .nofilter import name as _no_filter_name

class Filters(QtGui.QComboBox):
    """The drop in replacement for the filter selection combo box.

    This class takes iterates over all of the valid entry points
    provided in the group ``vtimshow.filters`` and populates it's combo
    box with the names of the entry points.  To be a valid entry point,
    the object referenced by the entry point must have a ``name``
    variable that provides a string to use in the combo box and a
    ``comupte(array)`` method that accepts a ``(N,H,W)`` array and
    either reduces it to a ``(H,W)`` array or returns ``None``.

    """

    def __init__(self, parent=None):
        """Initialize the filters combo box.

        Parameters
        ----------

        parent : :class:`PyQt4.QtGui.QWidget`
            The parent widget.

        """
        super(Filters, self).__init__(parent)
        self.find_filters()

    def find_filters(self):
        """Find all filters that pass a quick check.

        To pass the quick check, a filter must define a ``name``
        variable at the top scope of the plugin  that is a string and
        define a function named ``compute``.  All plugins that have both
        attributes are then added to the internal combo box.  The first
        item will be the :class:`nofilter` plugin because it is
        distributed with this class.  The remaining filters will be
        placed in alphabetical order.  If two plugins use the same name
        for the ``name`` attribute, a RuntimeError is raised.

        ..  note::  This method does not check if the plugin provides
                    the proper interface.  Specifically, it does not
                    check if the input takes the appropriate dimension
                    array or returns the proper array shape or ``None``
                    value.

        Raises
        ------

        RuntimeError:
            If two plugins have the same value in the ``name``
            attribute.

        """
        logger = logging.getLogger(__name__ +".Filters.find_filters")
        self.clear()
        group = ".".join(__name__.split(".")[:-1])
        dist = group.split(".")[0]
        self._plugins = {}
        for entry in pkg_resources.iter_entry_points(group):
            loaded = entry.load()
            try:
                if loaded.name in self._plugins:
                    msg = "{0:s} used twice!  Please contact the " \
                        +"author(s) of the plugins to establish a " \
                        +"unique name for each."
                    raise RuntimeError(msg.format(loaded.name))

                self._plugins[loaded.name] = loaded.compute
                if loaded.name == _no_filter_name:
                    # Add the guaranteed no filter item.
                    self.insertItem(0, loaded.name)

            except AttributeError as err:
                miss = str(err).split()[-1][1:-1]
                if miss in ("name", "compute"):
                    msg = "Skipping poorly formed filter {0:s}!  " \
                        "{2:s} is missing"
                    logger.warn(msg)
                else:
                    raise

        if self.count() == 0:
            raise RuntimeError("Required no filter plugin missing!")

        items = sorted(self._plugins)
        items.pop(items.index(_no_filter_name))
        self.insertItems(1, items)

    def apply(self, array):
        """Apply the current filter to the array.

        Get the current filter from the internal combo box and pass the
        array to that filter.  If a ``RuntimeError`` is encountered, it
        is reported to the logger as a warning and ``None`` is returned.

        Parameters
        ----------

        array : :class:`numpy.ndarray`
            The 3D image array to pass to the filter.

        Returns
        -------

        ret : :class:`numpy.ndarray` or ``None``
            The filtered array or ``None``

        """
        logger = logging.getLogger(__name__ +".Filters.apply")
        filt = self.currentText()
        try:
            ret = self._plugins[filt](array)
        except RuntimeError as err:
            msg = "Error applying {0:s}.  Message {1!s}"
            logger.warning(msg.format(filt, err))
            ret = None

        return ret

