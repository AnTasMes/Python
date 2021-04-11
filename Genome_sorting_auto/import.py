import os
from distutils.sysconfig import get_python_inc
from PyInstaller.utils.hooks import _find_prefix
print(_find_prefix(os.path.join(get_python_inc(), "pyconfig.h")))
print(_find_prefix(os.path.join(get_python_inc(True), "pyconfig.h")))