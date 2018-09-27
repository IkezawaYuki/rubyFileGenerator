from distutils.core import setup
import py2exe, sys, os


setup(
    options={"py2app": {"bundle_files": 1}},
    zipfile=None,
    console=[
        {"script": "entrance.py",
         "icon_resources":[(1, "entrance_image.ico")],
         }
    ]
)
