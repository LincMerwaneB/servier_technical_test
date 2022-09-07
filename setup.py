""" setup file """
import os
from setuptools import setup


def read(fname):
    """ Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open('requirements.txt') as file:
    required = file.read().splitlines()
setup(
    name="servier_technical_test",
    version="0.0.1",
    author="Merwane Bouali",
    author_email="andrewjcarter@gmail.com",
    description=("a data pipeline that generates a graph from csv file"),
    license="BSD",
    url="http://packages.python.org/an_example_pypi_project",
    packages=['src', 'tests'],
    install_requires=required,
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
