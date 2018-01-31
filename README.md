# JsonPydexer
A (python) indexer for large collections of json files.
In development and probably not good for general use yet.
`pip install JsonPydexer`

## Usage
### Starting from zero
```python
from JsonPydexer import JsonPydexer

# initialize with the root directory containing your json files
jp = JsonPydexer("test_data/1")

# index on your keys. provide a list of keynamess. keyname elements can be a string for a 
# field at root level, or a list of strings for nested fields
jp.index(["id", ["details", "name"]])
```
### Opening an existing index
```python
# initialize with the root directory containing your json files and .jp.pkl
jp = JsonPydexer("test_data/1")

# get all the files that match a search string for non-unique index
search_string = "Foo"
for filename in jp.get_files(["key_name"], search_string):
    with open(filename, "r") as f:
        print(f)

# get the file matching a search string for a unique index
search_string = "Bar"
with open(jp.get_file(["unique_key_name"], search_string), "r") as f:
    print(f)
```

### Added, removed, or modified JSON files? Updating
```python
jp = JsonPydexer("test_data/1")

jp.update()
```
New files in the directory will be added to the index. Coming soon are: removing files not present in the directory from the index, and checking for modified files in the directory.

