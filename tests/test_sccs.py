"""Test Strongly Connected Component Algorithms

"""
from __future__ import unicode_literals
import pytest
from graph_algo.graph import Graph
from os import path

file_dir = path.dirname(path.abspath(__file__))


@pytest.fixture
def scc_case1():
    return Graph.read_input_part1_hw4(path.join(file_dir, "testcases/part1_hw4_sccs_case1.txt"))


@pytest.fixture
def scc_case2():
    return Graph.read_input_part1_hw4(path.join(file_dir, "testcases/part1_hw4_sccs_case2.txt"))


@pytest.fixture
def scc_case3():
    return Graph.read_input_part1_hw4(path.join(file_dir, "testcases/part1_hw4_sccs_case3.txt"))


@pytest.fixture
def scc_case4():
    return Graph.read_input_part1_hw4(path.join(file_dir, "testcases/part1_hw4_sccs_case4.txt"))


@pytest.fixture
def scc_case5():
    return Graph.read_input_part1_hw4(path.join(file_dir, "testcases/part1_hw4_sccs_case5.txt"))
