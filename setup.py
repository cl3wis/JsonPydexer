from setuptools import setup, find_packages
from codecs import open
from os import path

import JsonPydexer as jp

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_desc = f.read()

setup(
    name="JsonPydexer",
    version="0.2.2",
    description="A (python) indexer for large collections of json files",
    long_description=long_desc,
    url="http://github.com/cl3wis/JsonPydexer",
    author=jp.__author__,
    author_email="me@christianbailey.me",
    license="MPL 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)"
    ],
    keywords="json index",
    packages=find_packages(),
    install_requires=[],
    python_requres=">=3",
    py_modules=["JsonPydexer"]
    )
