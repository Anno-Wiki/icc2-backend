import sys
import inspect
from .annotations import *
from .users import *

classes = dict(inspect.getmembers(sys.modules[__name__], inspect.isclass))
