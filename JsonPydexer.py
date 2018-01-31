__author__ = "Christian Bailey (me@christianbailey.me)"
__version__ = "0.3.0"

import os
import json
import pickle
import sys
import stat
from Index import Index
from pathlib import Path
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
        self.index_obj = self.load()


    def index(self, keys, r=True):
        """Index .json files in the root path. Pickles the Index object which can
        be loaded later.

        Args:
            keys (list): list of keys. each element can be a string, in the case of
            a key field at the root level of the json document, or a list of strings,
            in the case of a key field that is nested within other fields
            r (bool, optional): recurse into lower directories or not. not yet
            implemented
        Returns: None
        """
        if type(keys) is str:
            raise ValueError("keys argument must be a list of strings or lists")
        keys = [self.key_name_to_tuple(key) for key in keys]

        if self.index_obj:
            # we will use update methods
            self.index_obj.add_key_names(keys)
            self.update()
        else:
            # we will use create methods
            self.index_obj = Index(keys, self.rootPath)
            self.update()


    def key_name_to_tuple(self, key_name):
        """Convert a key_name, either as list or string, into a tuple for hashing

        Args:
            key_name: either a string or list of strings.
        Returns: Tuple
        """
        if type(key_name) is str:
            return tuple([key_name])
        elif type(key_name) is list:
            return tuple(key_name)


    def update(self):
        """Remove deleted files from the Index, add new files to the Index. Removing
        deleted files has not been tested.
        """
        # load filenames in I as set_I
        set_I = set(self.index_obj.files)

        # load filenames in rootpath as set_F
        p = Path(self.rootPath)
        files = p.glob("**/*.json")
        set_F = set([str(f.relative_to(self.rootPath)) for f in files])

        # remove zombies (remove set(set_I - set_F) from index and set_I
        #TODO write a test for htis
        zombies = set_I - set_F
        for zombie in zombies:
            self.index_obj.remove(zombie)
            set_I.remove(zombie)

        #TODO issue #24 update modified files
        # for i in set_I
            # if (index -> files -> I -> timestamp) < (rootpath -> I -> timestamp)
                # index.update(I)
                # remove I from set_I

        # add new files from set_F (eg set_F - set_I) to I
        newfiles = set_F - set_I
        for newfile in newfiles:
            self.index_obj.add(newfile)

        with open(".jp.pkl", mode="wb") as f:
            pickle.dump(self.index_obj, f)


    def load(self):
        """Try to open the Index object pickled at rootpath
        Returns: Index or False
        """
        path = Path(self.rootPath, ".jp.pkl")
        if path.is_file():
            with open(str(path), "rb") as f:
                return pickle.load(f)
        else:
            return False


    def get_file(self, key_name, needle):
        """Get the file with a unique index matching the needle
        Args:
            key_name (list): a key_name, formatted the same way as a single element
            of the key_names list used when calling index()
            needle (string): your search term
        Returns: filename
        """
        key_name = self.key_name_to_tuple(key_name)
        if key_name in self.index_obj.unique_indices:
            return self.index_obj.unique_indices[key_name].get(needle, False)
        else:
            raise ValueError("Error: Invalid Key. Check in group_indices")

    def get_files(self, key_name, needle):
        """Get the files with a non-unique index matching the needle:
            key_name (list): a key_name, formatted the same way as a single element
            of the key_names list used when calling index()
            needle (string): your search term
        Returns: generator
        """
        key_name = self.key_name_to_tuple(key_name)
        if key_name in self.index_obj.group_indices:
            for filename in self.index_obj.group_indices[key_name].get(needle, []):
                yield filename
        else:
            raise ValueError("Error: Invalid Key. Check in unique_indices")

