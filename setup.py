import sys
import os
from cx_Freeze import setup, Executable

files = ['ccrlogo.ico']

target = Executable(script = "GUI.py", base = "Win32GUI", icon = "ccrlogo.ico")

setup(name = "CPG_GUI", version = "1.0", description = "GUI for the CPG senior design project", author = "Brandt Walton", options = {'build_exe' : {'include_files' : files}}, executables = [target])