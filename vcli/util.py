
import views
import io
import os

import joblib
import pyarrow

import hashlib
import logging

logger = logging.getLogger(__name__)

DISPATCH = {
        ".parquet": (pyarrow.parquet.write_table, pyarrow.parquet.read_table),
        ".joblib": (joblib.dump, joblib.load)
    }

def typeFilePath(checksum):
    return os.path.join(views.DIR_STORAGE,"cache","types",checksum)

def checkType(p):
    _,ext = os.path.splitext(p)
    _,load = DISPATCH[ext]
    with open(p,"rb") as f:
        raw = f.read()
        h = hashlib.md5(raw)
    try:
        with open(typeFilePath(h.hexdigest()),"rb") as f:
            logger.debug(f"Using cache to check type of {p}")
            return joblib.load(f)
    except FileNotFoundError:
        logger.debug(f"Cache not found when checking type of {p}")
        fileobject = io.BytesIO(raw)
        t = type(load(fileobject))
        with open(typeFilePath(h.hexdigest()),"wb") as f:
            joblib.dump(t,f)
        return t
