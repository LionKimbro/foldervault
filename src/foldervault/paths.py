"""foldervault.paths

Note: 
"""
import pathlib

from .words import *
from . import foldervault


def pathfor(sym):
    if sym == LOCKS:
        return foldervault.g[PATH] / "locks"
    elif sym == DATA:
        return foldervault.g[PATH] / "data"
    else:
        raise ValueError(sym)

