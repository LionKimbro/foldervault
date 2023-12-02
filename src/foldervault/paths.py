"""foldervault.paths

MIT License

Copyright (c) 2023 Lion Kimbro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import pathlib

from .words import *


kFOLDERVAULTDIR_ENVIRONMENTVAR = "FOLDERVAULTDIR"
kFOLDERVAULTDIR_DEFAULT = ".foldervault"

def pathfor(sym):
    from . import foldervault
    
    if sym == FOLDERVAULTDIR: # config directory
        # 1. check for environment var
        #
        env_path = os.environ.get(kFOLDERVAULTDIR_ENVIRONMENTVAR)
        
        if env_path:
            # If environment variable set, return Path based on
            # environment var.
            #
            return pathlib.Path(env_path)
        else:
            # If environment variable NOT set, return Path based on
            # home directory.
            #
            # "~/.foldervault"
            #
            return pathlib.Path.home() / kFOLDERVAULTDIR_DEFAULT
    
    elif sym == MAP:
        return pathfor(FOLDERVAULTDIR) / "diskmap.json"
    
    if sym == LOCKS:
        return foldervault.g[PATH] / "locks"
    
    elif sym == DATA:
        return foldervault.g[PATH] / "data"
    
    else:
        raise ValueError(sym)

