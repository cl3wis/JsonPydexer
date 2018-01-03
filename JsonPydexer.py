__author__ = "Christian Bailey (me@christianbailey.me)"
__version__ = "0.2.2"

import os
import json
import pickle
import sys
import stat
from functools import reduce
from operator import getitem

class JsonPydexer:
    """Base class for doing things"""
    def __init__(self, path):
        """Initialize class and check path

        Args:
            self: self
            path (str): path of directory containing files to index
        Returns:
            JsonPydexer: instance
        """
        self.rootPath = path

        # check that path is actually a directory
        if (stat.S_ISDIR(os.stat(self.rootPath).st_mode) == 0):
            raise ValueError("A non-directory file was passed")
        elif not (os.access(self.rootPath, os.W_OK)):
            raise ValueError("Specified directory is not writable")

    def give_me_indexes(r, key, self):
        index = dict()

        for root, subFolders, files in os.walk(self.rootPath):
            for file in files:
                name, extension = os.path.splitext(file)
                if extension == ".json":
                    with open(root + "/" + file) as f:
                        j = json.load(f)
                        try:
                            file_key = reduce(getitem, key, j)
                            if r:
                                index[file_key] = os.path.join(
                                    os.path.relpath(root, start=self.rootPath), file
                                )
                            else:
                                index[file_key] = file
                        except KeyError:
                            continue

        return index

    def index(self, key, r=False, filename=None):
        """Index .json files in the root path. Pickles the index as a dict, with
        whichever key you specify as the key and relative filenames as values to
        save on storage space.

        Args:
            key (list): list of keys. each element of the list is one level of a
            nested key
            r (bool, optional): recurse into lower directories or not. not yet
            implemented
            filename (string, optional): Filename to save the index as. defaulti
            is str(key) + ".pickle"
        Returns: None
        """
        if type(key) is str:
            key = [key]

        if filename is None:
            filename = ''.join(key + [".pickle"])

        if os.path.isfile(filename):
            raise ValueError("index file alreay exists")

        index = JsonPydexer.give_me_indexes(r, key, self)

        with open(filename, mode="wb") as f:
            pickle.dump(index, f)
