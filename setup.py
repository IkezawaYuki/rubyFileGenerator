import os
import sys

from cx_Freeze import setup, Executable


os.environ['TCL_LIBRARY'] = 'C:\\Users\\works\\Anaconda3\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = 'C:\\Users\\works\\Anaconda3\\tcl\\tk8.6'

build_exe_options = {}

base = None
if sys.platform == "win32":
        base = "Win32GUI"

directory_table = [
(
    "ProgramMenuFolder",
    "TARGETDIR",
    ".",
),
(
    "CalMyProgramMenu",
    "ProgramMenuFolder",
    "entrance",
),
                ]

msi_data = {
    "Directory": directory_table,
}

setup(
    name = "entrance",
    version = "4.0.1",
    description = "Entrance",
    options = {"build_exe": build_exe_options,
               'bdist_msi': { 'data': msi_data } },
    executables = [
        Executable(
            "entrance.py",
            base=base,
            shortcutName="entrance",
            shortcutDir="CalMyProgramMenu",
            )
        ])
