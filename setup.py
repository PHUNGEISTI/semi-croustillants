"""Fichier d'installation de notre script salut.py."""
#import numpy.core._methods
#import numpy.lib.format
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

from cx_Freeze import setup, Executable
additional_mods = ['numpy.core._methods', 'numpy.lib.format','scipy.sparse.csgraph._validation']

# On appelle la fonction setup
setup(
    name = "JohnsonElectricPredictions",
    version = "0.1",
    description = "Ce programme vous ouvre une interface de prédiction au localhost:8085",
    options = {'build_exe': {'includes': additional_mods}},
    executables = [Executable("interfaceweb.py")],
)