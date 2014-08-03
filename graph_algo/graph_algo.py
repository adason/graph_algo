# -*- coding: utf-8 -*-
"""Main program for Command Line interface

Usage:
    graph_algo [-hv] (-i <file>)
    graph_algo --version

Options:
    -h --help             show this help message and exit
    --version             show version and exit
    -v --verbose          print status messages
    -i, --input <file>    input file

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
