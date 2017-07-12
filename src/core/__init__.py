"""
core package

flo behaviors

"""
from __future__ import generator_stop

import sys
import importlib

from ioflo.aid.sixing import *

_modules = ['resting', 'behaving', ]

for m in _modules:
    importlib.import_module(".{0}".format(m), package='bluepea.core')
