ViTables Image Viewer
=====================

This is a plug-in to [ViTables] to view data sets as images.  It uses
[PyQtGraph] to visualize the data sets in the workspace.  Valid viewable
data sets include 2D arrays (H,W) as monochrome images, 3D arrays as
RGB(A) (H,W,3) with or without the alpha channel, 3D arrays as N
monochrome images (N,H,W), and 4D arrays as N RGB(A) images (N,H,W,3).
A long term goal is to answer the problems addressed in [Issue #11].

This plug-in is designed to work with the development branch of ViTables
(2.2a1), and, therefore, uses `setuptools` to declare the entry points
into `vitables.plugins`.

Screen Shot
-----------

![Viewing example/example.h5](example/screen_shot_20150521T140720.png)


Installation
------------

First, ensure that the correct version of [ViTables] and [PyQtGraph] are
installed.  The minimum version of ViTables necessary is (2.2a1) which
is currently the development branch.  The lowest know version of
PyQtGraph that has been tested is 0.9.10.  Once those dependencies have
been installed, run

    python setup.py install

After running the install, launch ViTables, open the Preferences menu,
select the Plugins tab, and enable Image Viewer.  Once you restart
ViTables, you can right click on a data set and view it as an image.

Preferences
-----------

The default ordering of the arrays in the file is assumed to be (Depth,
Width, Height, RGB(A)).  To change this order, go to Preferences ->
image_viewer and select the proper order.  To have this persist, simply
hit save before exiting the preferences menu.

### Notes ###

As noted in [Issue #33], the current development branch of ViTables
requires `setuptools-git` to work.  If you need to install ViTables from
an archived download, please refer to [this patch] to aid in
installation.  Alternatively, you can download the patched version of
the development branch [here](patched vitables)

[ViTables]: http://vitables.org
[PyQtGraph]: http://www.pyqtgraph.org
[Issue #11]: https://github.com/uvemas/ViTables/issues/11
[Issue #33]: https://github.com/uvemas/ViTables/issues/33
[this patch]: https://github.com/kprussing/ViTables/commit/9ca932dc862704b30b7f49c997a35385cf59235c
[patched vitables]: https://github.com/kprussing/ViTables/tree/install_fix

