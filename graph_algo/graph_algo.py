# -*- coding: utf-8 -*-
"""Example of program with many options using docopt.

Usage:
    graph_algo [-hvqrf NAME] [--exclude=PATTERNS]
        [--select=ERRORS | --ignore=ERRORS] [--show-source]
        [--statistics] [--count] [--benchmark] PATH...
    graph_algo (--doctest | --testsuite=DIR)
    graph_algo --version

Arguments:
    PATH  destination path

Options:
    -h --help            show this help message and exit
    --version            show version and exit
    -v --verbose         print status messages
    -q --quiet           report only file names
    -r --repeat          show all occurrences of the same error
    --exclude=PATTERNS   exclude files or directories which match these comma
                         separated patterns [default: .svn,CVS,.bzr,.hg,.git]
    -f NAME --file=NAME  when parsing directories, only check filenames matching
                         these comma separated patterns [default: *.py]
    --select=ERRORS      select errors and warnings (e.g. E,W6)
    --ignore=ERRORS      skip errors and warnings (e.g. E4,W)
    --show-source        show source code for each error
    --statistics         count errors and warnings
    --count              print total number of errors and warnings to standard
                         error and set exit code to 1 if total is not null
    --benchmark          measure processing speed
    --testsuite=DIR      run regression tests from dir
    --doctest            run doctest on myself

"""


from __future__ import unicode_literals, print_function
from docopt import docopt


__version__ = "0.1.0"
__author__ = "Adason"
__license__ = "MIT"


def main():
    """Main entry point for the graph_algo CLI.
    """
    args = docopt(__doc__, version=__version__)
    print(args)