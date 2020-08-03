"""
Interface functions that make it dead simple to interact with ViEWS.
"""
import views
import os
import re

import joblib
import pyarrow

from typing import Callable,Any
from dataclasses import dataclass
from vcli.util import checkType

def viewspath(*args,**kwargs):
    return os.path.join(views.DIR_STORAGE,*args,**kwargs)

def fullpaths(path):
    return [os.path.join(path,p) for p in os.listdir(path)]

"""
Base class for listing and inspecting objects  
"""
@dataclass
class ViewsData:
    _name: str
    _test: Callable[[str],bool]
    _load: Callable[[str],Any]
    _dump: Callable[[str,Any],None]
    _inspect: Callable[[str],str]

    def _path(self):
        return viewspath(self._name)

    def _pathToName(self,path):
        return os.path.splitext(os.path.split(path)[-1])[0]

    def list(self):
        """
        List all entries.
        """
        return [p for p in fullpaths(self._path()) if self._test(p)]

    def get(self,name):
        """
        Get entry path from name
        """
        e = [p for p in self.list() if self._pathToName(p) == name]
        return e[0] if e else None

    def inspect(self,name):
        return self._inspect(self._load(self.get(name)))

Model = ViewsData(
        _name = "models",
        _test = lambda p: checkType(p) is views.apps.model.Model,
        _load = joblib.load,
        _dump = joblib.dump,
        _inspect = lambda x: str(x)
    ) 
Model.__doc__ = "Manage models"

Dataset = ViewsData(
        _name = "data/datasets",
        _test = lambda p: checkType(p) is pyarrow.lib.Table,
        _load = pyarrow.parquet.read_table,
        _dump = pyarrow.parquet.write_table,
        _inspect = lambda x: "not implemented"
        )
Dataset.__doc__ = "Manage datasets"
