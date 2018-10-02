
from distutils.core import setup
import py2exe

option = {
    'bundle_files': 1,
    'compressed': 1,
    'optimize': 2
}
setup(
    options={
        'py2exe': option
    },
    windows=[
        {"script": "entrance.py"}
    ],
    zipfile=None
)
