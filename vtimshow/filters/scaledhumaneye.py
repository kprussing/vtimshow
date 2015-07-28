#!/usr/bin/env python3
_datafile = ""
__doc__="""The human eye response filters.

This collects the filters for applying the scaled spectral response of
the human eye to the provided array

..  math::  \\int_0^1 \\overbar{R}(u)I(Nu) du

where :math:`\\overbar{R}(u)` is the red, blue or green spectral
response of the human eye scaled such that the response is in the range
:math:`[0.0, 1.0]`, the wavelengths have been mapped to :math:`u \\in
[0.0, 1.0]`, and :math:`N = \\text{(Number of frames)} - 1` is the
number of frames in the image less one.  The values for the wavelengths
and response are taken from the first and second columns of the file
'stockman_spectral_2000-table-3.csv' distributed with this filter
respectively.  To evaluate the integral, we only have to evaluate the
spectral response at :math:`I/(N-1)` for each frame.

"""
import pkg_resources
import numpy
import scipy.interpolate

def apply_spectrum(array, color):
    """Apply the ``color`` spectrum to ``array``.

    Compute 

    ..  math::  \\sum_{n=0}^{N-1} \\overbar{R}(\\frac{n}{N-1) I_{n,m}

    where :math:`\\overbar{R}` is the red, green, or blue scaled
    spectrum specified in ``color`` and :math:`I_{n,m}` is the nth frame
    of the mth image in ``array``.

    Parameters
    ----------

    array : :class:`numpy.ndarray`
        The array to apply the spectrum.
    color : string
        Either 'red', 'green', or 'blue'

    Returns
    -------

    ret : :class:`numpy.ndarray`
        The reduced image.

    Raises
    ------

    RuntimeError
        If ``array`` is not 3D.

    """
    if array.ndim != 3:
        raise RuntimeError(
            "Invalid array with dimension {0:d}".format(array.ndim)
        )

    if color not in _spectrum:
        msg = "Unknown response {0!s}!  Should be in {1!s}"
        raise RumtimeError(msg.format(color, list(_spectrum.keys())))

    xx = numpy.linspace(0, array.shape[0] -1) /(array.shape[0] -1)
    yy = scipy.interpolate.splev(xx, _spectrum[color]).reshape(
        (array.shape[0], 1, 1)
    )
    ret = numpy.sum(yy *array, axis=0)
    return ret

def load_spline_data(csvfile="stockman_spectral_2000-table-3.csv"):
    """Read the given CSV file and compute the spline parameters.

    Assume that the CSV file has four columns.  The first column is the
    wavelength, and the second through fourth are the red, blue, and
    green responses respectively.  Then, independently scale each column
    to the range [0,1].  Next, compute the spline parameters for each
    wavelength/color combination and store the result in a dictionary
    using the color as the key.

    Parameters
    ----------

    csvfile : string
        The path to the CSV file to be passed to
        :`func`pkg_resources.resource_stream`.

    Returns
    -------

    ret : dict
        The dictionary of spline parameters accessed by color.

    Raises
    ------

    RuntimeError
        If ``csvfile`` does not have four columns.

    """
    data = numpy.loadtxt(
        pkg_resources.resource_stream(__name__, csvfile),
        delimiter=","
    )
    if data.shape[1] != 4:
        raise RuntimeError(
            "{0:s} does not have four columns!".format(csvfile)
        )

    colors = ("red", "green", "blue")
    ret = {}
    XX = (data[:,0] -min(data[:,0])) /(max(data[:,0]) -min(data[:,0]))
    for color in colors:
        idx = colors.index(color) +1
        YY = (data[:,idx] -min(data[:,idx])) \
            / (max(data[:,idx]) -min(data[:,idx]))
        ret[color] = scipy.interpolate.splrep(XX, YY)

    return ret

_spectrum = load_spline_data()

class Red:
    """The human eye scaled red response."""
    name = "Scaled red"
    """Filter name"""

    def compute(self, array):
        """Apply the scaled red human eye response.
        
        Call :func:`apply_spectrum` with ``color='red'``.

        Parameters
        ----------

        array : :class:`numpy.ndarray`
            The array to process

        Returns
        -------

        ret : :class:`numpy.ndarray`
            The reduced image.

        """
        return apply_array(array, "red")

class Green:
    """The human eye scaled green response."""
    name = "Scaled green"
    """Filter name"""

    def compute(self, array):
        """Apply the scaled green human eye response.
        
        Call :func:`apply_spectrum` with ``color='green'``.

        Parameters
        ----------

        array : :class:`numpy.ndarray`
            The array to process

        Returns
        -------

        ret : :class:`numpy.ndarray`
            The greenuced image.

        """
        return apply_array(array, "green")

class Blue:
    """The human eye scaled blue response."""
    name = "Scaled blue"
    """Filter name"""

    def compute(self, array):
        """Apply the scaled blue human eye response.
        
        Call :func:`apply_spectrum` with ``color='blue'``.

        Parameters
        ----------

        array : :class:`numpy.ndarray`
            The array to process

        Returns
        -------

        ret : :class:`numpy.ndarray`
            The blueuced image.

        """
        return apply_array(array, "blue")

