""" setup file """

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "servier_technical_test",
    version = "0.0.1",
    author = "Merwane Bouali",
    author_email = "andrewjcarter@gmail.com",
    description = ("a data pipeline that generates a graph from csv file"),
    license = "BSD",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['src', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)