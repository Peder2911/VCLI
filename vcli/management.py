
import views
import os
import logging
import json

import vcli.interface

class storage():
    path = None 
    dataclass = None
    _deserializer = json.load
    _serializer = json.dump

    @classmethod
    def folder(cls):
        return os.path.abspath(os.path.join(views.DIR_STORAGE,cls.path))

    @classmethod
    def list(cls):
        """
        Shows a list of {cls.folder}
        """
        return [*os.listdir(cls.folder())]

    @classmethod
    def save(cls,obj,path):
        with open(os.path.join(cls.folder(),path),"w") as f:
            cls._serializer(obj,f)

    @classmethod
    def load(cls,path):
        with open(os.path.join(cls.folder(),path),"r") as f:
            return cls._deserializer(f)

class Management:
    models = vcli.interface.Model
    datasets = vcli.interface.Dataset

