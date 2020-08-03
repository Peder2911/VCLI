
import unittest
import vcli
import views
import os
import joblib

class TestVcli(unittest.TestCase):
    def test_path_interface(self):
        modelPath = vcli.interface.viewspath("models")
        self.assertEqual(os.path.join(views.DIR_STORAGE,"models"),modelPath)

        for p in vcli.interface.listmodels():
            with open(p,"rb") as f:
                self.assertIs(type(joblib.load(f)),views.apps.model.Model)
