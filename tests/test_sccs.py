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


def scc_sizes(g):
    sizes = []
    for scc in g.kosaraju_sccs():
        print(scc)
        sizes.append(len(scc))
    return sorted(sizes, reverse=True)


def test_scc_sizes_case1(scc_case1):
    assert scc_sizes(scc_case1) == [3, 3, 3]


@pytest.fixture
def scc_case2():
    return Graph.read_input_part1_hw4(path.join(file_dir, "testcases/part1_hw4_sccs_case2.txt"))


def test_scc_sizes_case2(scc_case2):
    assert scc_sizes(scc_case2) == [3, 3, 2]


@pytest.fixture
def scc_case3():
    return Graph.read_input_part1_hw4(path.join(file_dir, "testcases/part1_hw4_sccs_case3.txt"))


def test_scc_sizes_case3(scc_case3):
    assert scc_sizes(scc_case3) == [3, 3, 1, 1]


@pytest.fixture
def scc_case4():
    return Graph.read_input_part1_hw4(path.join(file_dir, "testcases/part1_hw4_sccs_case4.txt"))


def test_scc_sizes_case4(scc_case4):
    assert scc_sizes(scc_case4) == [6, 3, 2, 1]


# @pytest.fixture
# def scc_case5():
#     return Graph.read_input_part1_hw4(path.join(file_dir, "testcases/part1_hw4_sccs_case5.txt"))


# def test_scc_sizes_case5(scc_case5):
#     assert scc_sizes(scc_case5)[0:5] == [917, 313, 167, 37, 3]
