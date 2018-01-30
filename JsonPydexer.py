__author__ = "Christian Bailey (me@christianbailey.me)"
# TODO update version
__version__ = "x.x.x"

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


    def index(self, keys, r=True):
        """Index .json files in the root path. Pickles the index as a dict, with
        whichever key you specify as the key and relative filenames as values to
        save on storage space.

        Args:
            key (list): list of keys. each element of the list is one level of a
            nested key
            r (bool, optional): recurse into lower directories or not. not yet
            implemented
        Returns: None
        """
        if type(keys) is str:
            raise ValueError("keys argument must be a list of strings or iterables yielding strings")
        keys = [tuple([key]) if type(key) is str else tuple(key) for key in keys]

        if os.path.isfile(os.path.join(self.rootPath, ".jp.pkl")):
            # we will use update methods
            index = self.load()
        else:
            # we will use create methods
            index = Index(keys, self.rootPath)

        # load filenames in I as set_I
        set_I = set(index.files)

        # load filenames in rootpath as set_F
        p = Path(self.rootPath)
        files = p.glob("**/*.json")
        set_F = set([str(f.relative_to(self.rootPath)) for f in files])

        # remove zombies (remove set(set_I - set_F) from index and set_I
        zombies = set_I - set_F
        for zombie in zombies:
            index.remove(zombie)
            set_I.remove(zombie)

        #TODO update modified files
        # for i in set_I
            # if (index -> files -> I -> timestamp) < (rootpath -> I -> timestamp)
                # index.update(I)
                # remove I from set_I

        # add new files from set_F (eg set_F - set_I) to I
        newfiles = set_F - set_I
        for newfile in newfiles:
            index.add(newfile)

        with open(".jp.pkl", mode="wb") as f:
            pickle.dump(index, f)

