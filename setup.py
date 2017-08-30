# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 17:54:46 2017
setup.py
@author: imtiaz.a.khan
"""

from cx_Freeze import setup, Executable

base = None


executables = [Executable("test.py", base=base)]

packages = ["webbrowser"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "test",
    options = options,
    version = "1.0",
    description = 'test file',
    executables = executables
)
