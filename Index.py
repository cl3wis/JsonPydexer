import time
import json
from functools import reduce
from operator import getitem
from pathlib import Path

class Index:
    def __init__(self, key_names, rootPath, filename=None):
        self.files = dict()
        self.unique_indices = { key_name: {} for key_name in key_names }
        self.group_indices = dict()
        self.rootPath = rootPath


    def add(self, filename):
        with open(str(Path(self.rootPath, filename)), "r") as f:
            f = json.load(f)

            # update the filelist so we know we have handled this file at this time
            self.files[filename] = int(time.time())

            # check each of the unique_indices key names
            key_names = list(self.unique_indices)
            for key_name in key_names:
                # get the value in the file that we will index on
                key = reduce(getitem, key_name, f)

                # if we don't already have a filename for this key, add this filename 
                if not self.unique_indices.get(key_name).get(key, False):
                    self.unique_indices[key_name][key] = filename
                # else we already had a filename for this key, the key_name is no longer
                # a unique identifier. move it to group_indices. we don't need to add the
                # new file yet, since adding nonunique (group) indexes happens after this
                else:
                    self.move_unique_to_group(key_name)

            # check each of the group_indices key names
            for key_name in self.group_indices:
                # get the value in the file that we will index on
                key = reduce(getitem, key_name, f)

                # if we have already added the key to the group_keys[keyname], just
                # add our filename to the set for that key. otherwise, we must add
                # key to group_keys[keyname]
                if self.group_indices[key_name].get(key, False):
                    self.group_indices[key_name][key].add(filename)
                else:
                    self.group_indices[key_name][key] = set([filename])


    def move_unique_to_group(self, key_name):
        # create the new key_name in group_indices
        self.group_indices[key_name] = dict()

        # add each key,value pair in the unique key_name to the group key_name
        for key, value in self.unique_indices[key_name].items():
            self.group_indices[key_name][key] = set([value])
        # delete the key_name from the unique key_names
        del self.unique_indices[key_name]

