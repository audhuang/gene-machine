
from distutils.core import setup
from Cython.Build import cythonize
 
# Use "python setup.py build ---build-dir ." to compile

setup(
    name = "metro_simulator",
    ext_modules = cythonize( "metro.pyx")
)