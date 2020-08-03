import views 
import fire 
import sklearn

import os
import logging

from vcli.management import Management
from vcli.actions import Actions 

import vcli.interface

class ViEWS(Management,Actions):
    def __init__(self):
        if os.getenv("VIEWS_VERBOSE"):
            logging.basicConfig(level = logging.DEBUG)

if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG)
    fire.Fire(ViEWS)
