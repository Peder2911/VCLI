
import views
import os
import logging
import json

class spec():
    name = None 
    dataclass = None
    _deserializer = json.load
    _serializer = json.dump

    @classmethod
    def folder(cls):
        return os.path.abspath(os.path.join(views.DIR_STORAGE,cls.name))

    @classmethod
    def list(cls):
        """
        Shows a list of {cls.folder}
        """
        return [*os.listdir(cls.folder())]

    @classmethod
    def save(cls,obj,name):
        with open(os.path.join(cls.folder(),name),"w") as f:
            cls._serializer(obj,f)

    @classmethod
    def load(cls,name):
        with open(os.path.join(cls.folder(),name),"r") as f:
            return cls._deserializer(f)

class Management:

    class models(spec):
        name = "models"

    class periods(spec):
        name = "periods"

    class logs(spec):
        name = "logs"

