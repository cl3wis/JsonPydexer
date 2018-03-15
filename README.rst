JsonPydexer
===========

A (python) indexer for large collections of json files. In development
and probably not good for general use yet. 

Installation
------------

``pip install JsonPydexer``

Usage
-----

Starting from zero
~~~~~~~~~~~~~~~~~~

.. code:: python

    >>>from JsonPydexer import JsonPydexer
    >>># initialize with the root directory containing your json files
    >>>jp = JsonPydexer("test_data/3")
    >>># index on your keys. provide a list of keynamess. keyname elements can be a string for a 
    >>># field at root level, or a list of strings for nested fields
    >>>jp.index(["id", "name", ["field_in_root", "field_below"]])

Opening an existing index
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>># initialize with the root directory containing your json files and .jp.pkl
    >>>jp = JsonPydexer("test_data/3")
    >>># get all the files that match a search string for non-unique index
    >>>search_string = "alice"
    >>>for filename in jp.get_files(["name"], search_string):
    >>>    print(filename)
    1.json
    3.json
    >>># get the file matching a search string for a unique index
    >>>filename = jp.get_file(["id"], "id2")
    >>>print(filename)
    2.json

Added, removed, or modified JSON files? Update the index
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>>jp = JsonPydexer("test_data/3")
    >>>jp.update()

New files in the directory will be added to the index. Coming soon are:
removing files not present in the directory from the index, and checking
for modified files in the directory.
