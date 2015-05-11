#!/usr/bin/env python3
import os

from setuptools import setup, find_packages


from vtimshow import _defaults

def read(fname):
    """
    Utility function to read a file.
    """
    return open(fname, "r").read().strip()

setup(
    name = "vtimshow",
    version = read(os.path.join(os.path.dirname(__file__), "VERSION")),
    packages = find_packages(),

    description = _defaults["COMMENT"],
    long_description = read(
        os.path.join(os.path.dirname(__file__), "README.txt")
    ),

    author = _defaults["AUTHOR"],
    author_email = _defaults["AUTHOR_EMAIL"],
    license = _defaults["LICENSE"],

    install_requires = ["ViTables >2.1", "pyqtgraph"],
    dependency_links = [
        "https://github.com/uvemas/ViTables@f6cb68227e10bf0658fd11b8daa56b76452b0341#egg=project-version"
    ],

    entry_points = {
        "vitables.plugins" : 
        _defaults["UID"] +" = vtimshow:VtImageViewer"
    }
)
