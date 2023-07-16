import os
import sys

this = sys.modules[__name__]
# Two underscore to make it private
this.__CASIO_ROOT__ = os.path.dirname(os.path.realpath(__file__))


def switch_casio_root(root: str) -> None:
    this.__CASIO_ROOT__ = root
