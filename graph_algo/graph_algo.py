# -*- coding: utf-8 -*-
"""Main program for Command Line interface

Usage:
    graph_algo -h
    graph_algo --version
    graph_algo p2hw4 [--argo <argo>] [-v] -i <file>...

Options:
    -h --help                show this help message and exit
    --version                show version and exit
    -v --verbose             print status messages
    -i, --input <file>...    input file(s)
    --argo <algo>            choose one algorithm

"""


from __future__ import unicode_literals, print_function
from docopt import docopt
from .graph import Graph


__version__ = "0.1.0"
__author__ = "Adason"
__license__ = "MIT"


def main():
    """Main entry point for the graph_algo CLI.
    """
    args = docopt(__doc__, version=__version__)
    # print(args)

    if args["p2hw4"]:
        min_dists = []
        for fn in args["--input"]:
            g = Graph.read_input_part2_hw4(fn)
            dist_pairs = g.floyd_warshall_apsp()
            if dist_pairs:
                min_dists.extend(dist_pairs.values())
        if len(min_dists) > 0:
            print(min(min_dists))
        else:
            print("NULL")
