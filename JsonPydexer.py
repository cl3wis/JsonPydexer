__author__ = "Christian Bailey (me@christianbailey.me)"
__version__ = "0.0.1"

import os
import json
import pickle
import sys
import stat

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
            print("Error: {} is not reported as a directory.".format(self.rootPath), file=sys.stderr)
            raise ValueError("A non-directory file was passed")
        elif not (os.access(self.rootPath, os.W_OK)):
            raise ValueError("Specified directory is not writable")

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
        #TODO implement list of keys instead of surface level only 
        if filename is None:
            filename = ''.join([key, ".pickle"])
        #TODO check if filename already exists, 

        index = dict()
        for root, subFolders, files in os.walk(self.rootPath):
            for file in files:
                name, extension = os.path.splitext(file)
                if extension == ".json":
                    with open(root + "/" + file) as f:
                        j = json.load(f)
                        index[j[key]] = file
        with open(filename, mode="wb") as f:
            pickle.dump(index, f)

