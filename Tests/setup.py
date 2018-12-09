"""
Pour faire des exe (non fonctionnel)
"""

from cx_Freeze import setup, Executable
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None    

executables = [Executable("interfaceweb.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
        'includes':['pandas','numpy','sklearn','sklearn.metrics','math','matplotlib.pyplot','flask','io','base64','urllib.parse','werkzeug','numpy.core._methods', 'numpy.lib.format','sklearn._arpack'],
    },    
}

setup(
    name = "Test",
    options = options,
    version = "1",
    description = 'Lorem Ipsum',
    executables = executables
)
