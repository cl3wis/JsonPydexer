import unittest
import pickle
import os
from JsonPydexer import JsonPydexer

class PydexerConstructor(unittest.TestCase):
    good_dir = "test_data/1"
    not_dir = "test_data/file.txt"
    bad_perms = "test_data/bad_perms"

    def setUp(self):
        if not os.path.exists(self.bad_perms):
            os.makedirs(self.bad_perms, mode=0o000)


    def test_constructor(self):
        jp = JsonPydexer(self.good_dir)
        self.assertEqual(jp.rootPath, self.good_dir)


    def test_constructor_no_perms(self):
        with self.assertRaises(ValueError):
            jp = JsonPydexer(self.bad_perms)


    def test_constructor_not_dir(self):
        with self.assertRaises(ValueError):
            jp = JsonPydexer(self.not_dir)


    def tearDown(self):
        os.rmdir(self.bad_perms)


class PydexerIndex(unittest.TestCase):
    good_dir = "test_data/1"
    recursive_dir = "test_data/2"

    def test_index(self):
        jp = JsonPydexer(self.good_dir)
        jp.index("_id")
        with open("_id.pickle", "rb") as f:
            index = pickle.load(f)
            os.remove("_id.pickle")
            expectedDict = {
                "5a0a0239b4b70140c8827119": "1.json",
                "5a0a023902ee870ad28cd939": "2.json",
                "5a0a0239ef483b81585699c5": "3.json",
                "5a0a0239a78b6240acaebdb5": "4.json",
                "5a0a02399416569dc1f3fedd": "5.json"
            }
            self.assertEqual(index, expectedDict)


    def test_index_filename_exists(self):
        jp = JsonPydexer(self.good_dir)
        jp.index("_id")
        with self.assertRaises(ValueError):
            jp.index("_id")
        os.remove("_id.pickle")


    def test_index_recursive(self):
        jp = JsonPydexer(self.recursive_dir)
        jp.index("_id", r=True)
        with open("_id.pickle", "rb") as f:
            index = pickle.load(f)
            os.remove("_id.pickle")
            expectedDict = {
                "5a0a0239b4b70140c8827119": "a/1.json",
                "5a0a023902ee870ad28cd939": "a/2.json",
                "5a0a0239ef483b81585699c5": "a/aa/3.json",
                "5a0a0239a78b6240acaebdb5": "b/4.json",
                "5a0a02399416569dc1f3fedd": "./5.json"
            }
            self.assertEqual(index, expectedDict)


    def test_index_nested_key(self):
        jp = JsonPydexer(self.good_dir)
        jp.index(["foo", "guid"])
        with open("fooguid.pickle", "rb") as f:
            index = pickle.load(f)
            os.remove("fooguid.pickle")
            expectedDict = {
                "9d634636-c7a3-48d1-9ec7-5fc91e50aaf4": "1.json",
                "4d7c74f3-0cb8-4287-a7da-2b124f325dea": "2.json",
                "fa75756f-8fbd-4848-9d2f-5ee9df0f149f": "3.json",
                "a1b422cb-e54b-4359-aa4f-3b486ce858a0": "4.json",
                "c11c222d-0f07-4984-b240-a0a4e22ddcf8": "5.json"
            }
            self.assertEqual(index, expectedDict)


if __name__ == '__main__':
    unittest.main()

