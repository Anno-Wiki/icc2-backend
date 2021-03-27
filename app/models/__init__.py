import pkgutil
import os
import importlib
from .mixins import Base

pkg_dir = os.path.dirname(__file__)

for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
    importlib.import_module('.' + name, __package__)

classes = {cls.__name__: cls for cls in Base.__subclasses__()}
