#!/usr/bin/env python3
import os

from setuptools import setup, find_packages

def read(fname):
    """
    Utility function to read a file.
    """
    return open(fname, "r").read().strip()

def find_package_datafiles(package):
    """
    Search a package for data files.

    Given a package, replace all occurrences of the '.' with '/' and
    search the directory for any file that is not a '.py' or '.pyc' file
    and add it to the list.  For each directory in the package, check to
    see if it is a package by checking for the '__init__.py' file.  If
    it is not a subpackage, recursively search it for more data files.

    """
    pkg_root = package.replace('.', '/')
    output = []
    fignores = ('.py', '.pyc')
    dignores = ('.git', '__pycache__')
    for filename in os.listdir(pkg_root):
        if filename in dignores:
            continue

        path = pkg_root + '/' + filename
        if os.path.islink(path):
            continue

        if os.path.isfile(path):
            if os.path.splitext(path)[1] not in fignores:
                output.append(filename)

        elif os.path.isdir(path):
            if os.path.exists(path + '/__init__.py'):
                # The subpackages are handled separately.
                continue

            for root, dirs, files in os.walk(path):
                print(root)
                for ignore in dignores:
                    if ignore in dirs:
                        dirs.remove(ignore)

                for dd in dirs:
                    if os.path.exists(dd + '/__init__.py'):
                        dirs.remove(dd)

                for ff in files:
                    if os.path.splitext(ff)[1] not in fignores:
                        # The path to the file is relative to the root
                        # of the package.  So, remove the package root.
                        fname = os.path.join(root, ff).replace('\\','/')
                        output.append(fname.replace(pkg_root + '/', ''))

    return output

setup(
    name = "vtimshow",
    version = read(os.path.join(os.path.dirname(__file__), "VERSION")).strip(),
    packages = find_packages(),

    description = "Display data sets as images",
    long_description = read(
        os.path.join(os.path.dirname(__file__), "README.markdown")
    ),

    author = "Keith F Prussing",
    author_email = "kprussing74@gmail.com",
    license = "MIT",

    install_requires = ["ViTables >2.1", "pyqtgraph"],
    dependency_links = [
        "https://github.com/uvemas/ViTables@f6cb68227e10bf0658fd11b8daa56b76452b0341#egg=project-version"
    ],

    entry_points = {
        "vitables.plugins" : "vtimshow = vtimshow:VtImageViewer"
    },

    package_data={
        pp : find_package_datafiles(pp) for pp in find_packages()
    }
)
