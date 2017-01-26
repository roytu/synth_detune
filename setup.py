from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    name = "Signals",
    ext_modules=[
        Extension("c_signals", ["c_signals.pyx"])
        ],
    cmdclass = {"build_ext": build_ext}
)
