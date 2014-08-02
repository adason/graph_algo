# -*- coding: utf-8 -*-
import re
from setuptools import setup


def find_version(fname):
    '''Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    '''
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version

__version__ = find_version("graph_algo/graph_algo.py")


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    name="graph_algo",
    version="0.1.0",
    description="A Collection of Graph Algorithms in Stanford Algorithm Course",
    long_description=read("README.rst"),
    author="Adason",
    author_email="tdadason@gmail.com",
    url="https://github.com/adason/graph_algo",
    install_requires=[
        "docopt"
    ],
    license=read("LICENSE"),
    zip_safe=False,
    keywords="graph_algo",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
    packages=[
        "graph_algo"
    ],
    package_dir={"graph_algo": "graph_algo"},
    entry_points={
        "console_scripts": [
            "graph_algo = graph_algo.graph_algo:main"
        ]
    }
)