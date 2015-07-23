#!/usr/bin/env python3
__doc__="""A collection of utility functions."""

import logging
import numpy

import vitables

def divide(A, B, rep=0.0):
    """Compute :math:`A / B` silencing warnings.

    Given two :class:`numpy.ndarray`, compute the element wise division
    suppressing divide by zero warnings and invalid entries.  All
    resulting NaNs, Infs, and places where ``B`` is essentially 0 are
    replaced by ``rep``.

    Parameters
    ----------

    A : :class:`numpy.ndarray`
        The numerator.
    B : :class:`numpy.ndarray`
        The denominator.
    rep : scalar, optional
        The value to replace bad values.

    Returns
    -------

    C : :class:`numpy.ndarray`
        ``A / B`` with bad values set to ``rep``.

    """
    with numpy.errstate(invalid="ignore", divide="ignore"):
        C = A / B

    C[numpy.isclose(B, 0)] = rep
    C[numpy.isnan(C)] = rep
    C[numpy.isinf(C)] = rep
    return C

def setup_logger(name):
    """Add the GUI's logging window as a stream handler.

    By default, the stream logger is removed during the invocation of
    ViTables.  The logging window in the GUI is a stream handler for the
    ViTables logger *only*.  This method will add the logging window in
    the GUI as a stream handler for the named logger.  The method checks
    to see if ViTables is an active application.  If it is not, nothing
    is done.

    Parameters
    ----------

    name : string
        The name of the module to add to the ViTables logging window.

    """
    logger = logging.getLogger(name)
    app = vitables.utils.getApp()
    if app is not None:
        stream = logging.StreamHandler(app.gui.logger)
        stream.setFormatter(
            logging.Formatter(vitables.vtgui._GUI_LOG_FORMAT)
        )
        logger.addHandler(stream)

    return

