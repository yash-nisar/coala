import os
import unittest
from collections import OrderedDict

from coalib.collecting.Importers import import_objects


class ImportObjectsTest(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.split(__file__)[0]
        test_dir = os.path.join(current_dir, "importers_test_dir")

        self.testfile1_path = {os.path.join(test_dir, "file_one.py"): test_dir}
        self.testfile2_path = {os.path.join(test_dir, "file_two.py"): test_dir}

        self.testfile12_path = dict(self.testfile1_path)
        self.testfile12_path.update(self.testfile2_path)

    def test_no_file(self):
        self.assertEqual(import_objects([]), [])

    def test_no_data(self):
        self.assertEqual(import_objects(self.testfile1_path), [])

    def test_name_import(self):
        self.assertEqual(
            len(import_objects(self.testfile12_path, names="name")),
            2)
        self.assertEqual(
            len(import_objects(self.testfile12_path, names="last_name")),
            0)

    def test_type_import(self):
        self.assertEqual(
            len(import_objects(self.testfile1_path,
                               types=list,
                               verbose=True)),
            2)
        self.assertEqual(
            len(import_objects(self.testfile12_path,
                               names="name",
                               types=OrderedDict,
                               verbose=True)),
            0)

    def test_class_import(self):
        self.assertEqual(
            len(import_objects(self.testfile12_path,
                               supers=list,
                               verbose=True)),
            1)
        self.assertEqual(
            len(import_objects(self.testfile12_path,
                               supers=str,
                               verbose=True)),
            0)

    def test_attribute_import(self):
        self.assertEqual(
            len(import_objects(self.testfile12_path,
                               attributes="method",
                               local=True,
                               verbose=True)),
            1)
        self.assertEqual(
            len(import_objects(self.testfile12_path,
                               attributes="something",
                               verbose=True)),
            0)

    def test_local_definition(self):
        self.assertEqual(
            len(import_objects(self.testfile12_path,
                               attributes="method",
                               verbose=True)),
            2)
        self.assertEqual(
            len(import_objects(self.testfile12_path,
                               attributes="method",
                               local=True,
                               verbose=True)),
            1)

    def test_invalid_file(self):
        for verbose in (True, False):
            with self.assertRaises(ImportError):
                import_objects({"some/invalid/path": "/"},
                               attributes="method",
                               local=True,
                               verbose=verbose)
