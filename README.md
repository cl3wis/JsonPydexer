# JsonPydexer
A (python) indexer for large collections of json files.
In development and probably not good for general use yet.
`pip install JsonPydexer`

## Usage
```python
from JsonPydexer import JsonPydexer

#initialize with the root directory containing your json files
jp = JsonPydexer("test_data/1")
# or with recursion
jp = JsonPydexer("test_data/1", r=True)

#index on the given key, creating the file _id.pickle, containing a pickled dict of _id: filename
jp.index("_id")

#index on the given list of nested keys ie {"foo": {"guid": value}}, creating the file fooguid.pickle
jp.index(["foo", "guid"])
```
