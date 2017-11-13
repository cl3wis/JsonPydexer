import unittest
import shutil, tempfile
from os import path
from JsonPydexer import JsonPydexer

class PydexerConstructor(unittest.TestCase):
    good_dir = "test_data/1"
    not_dir = "test_data/file.txt"

    def test_constructor(self):
        jp = JsonPydexer(self.good_dir)
        self.assertEqual(jp.rootPath, self.good_dir)


    def test_constructor_no_perms(self):
        """TODO: target for a future version"""
        pass


    def test_constructor_not_dir(self):
        with self.assertRaises(ValueError):
            jp = JsonPydexer(self.not_dir)


class PydexerIndex(unittest.TestCase):
    good_dir = "test_data/1"

    def test_index_no_filename(self):
        jp = JsonPydexer(self.good_dir)
        jp.index("_id")
        with open("_id.pickle") as f:
            index = pickle.load(f)
            #TODO assert for proper values here, not isnotnone
            self.assertIsNotNone(index)


    def test_index_filename(self):
        pass


    def test_index_recursive(self):
        pass


if __name__ == '__main__':
    unittest.main()

