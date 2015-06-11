#!/usr/bin/env python3
import os

from setuptools import setup, find_packages

def read(fname):
    """
    Utility function to read a file.
    """
    return open(fname, "r").read().strip()

setup(
    name = "vtimshow",
    version = read(os.path.join(os.path.dirname(__file__), "VERSION")),
    packages = find_packages(),

    description = "Display data sets as images",
    long_description = read(
        os.path.join(os.path.dirname(__file__), "README.rst")
    ),

    author = "Keith F Prussing",
    author_email = "kprussing74@gmail.com",
    url="https://github.com/kprussing/vtimshow/tree/stable",
    license = "MIT",

    install_requires = ["ViTables >2.1", "pyqtgraph"],
    dependency_links = [
        "https://github.com/uvemas/ViTables@f6cb68227e10bf0658fd11b8daa56b76452b0341#egg=project-version"
    ],

    entry_points = {
        "vitables.plugins" : "vtimshow = vtimshow:VtImageViewer"
    },

    package_data={"vtimshow" : ["*.ui"],},
)
