import unittest
import pickle
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
        with open("_id.pickle", "rb") as f:
            index = pickle.load(f)
            expectedDict = {
                "5a0a0239b4b70140c8827119": "1.json",
                "5a0a023902ee870ad28cd939": "2.json",
                "5a0a0239ef483b81585699c5": "3.json",
                "5a0a0239a78b6240acaebdb5": "4.json",
                "5a0a02399416569dc1f3fedd": "5.json"
            }
            self.assertEqual(index, expectedDict)

    def test_index_filename(self):
        pass


    def test_index_recursive(self):
        pass


if __name__ == '__main__':
    unittest.main()

