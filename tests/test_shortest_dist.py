"""Test graph class

"""
from __future__ import unicode_literals
import pytest
from graph_algo.graph import Graph
from os import path

file_dir = path.dirname(path.abspath(__file__))


@pytest.fixture
def g():
    g = Graph()
    g.add_vertice("1")
    g.add_vertice("2")
    g.add_vertice("3")
    g.add_edge("1", "1", "2", 2)
    g.add_edge("2", "2", "3", 1)
    g.add_edge("3", "3", "1", 3)
    return g


def test_dijstra_sd(g):
    assert g.dijstra_sd("1") == {"1": 0, "2": 2, "3": 3}


@pytest.fixture
def dijstra_case1():
    return Graph.read_input_part1_hw5(path.join(file_dir, "testcases/part1_hw5_dijstra_case1.txt"))


def test_dijstra_sd_case1(dijstra_case1):
    assert dijstra_case1.dijstra_sd("1") == {"1": 0, "2": 1, "3": 2, "4": 1, "7": 7, "6": 6, "5": 4}
    assert dijstra_case1.bellman_ford_sd("1") == {"1": 0, "2": 1, "3": 2, "4": 1, "7": 7, "6": 6, "5": 4}


@pytest.fixture
def dijstra_case2():
    return Graph.read_input_part1_hw5(path.join(file_dir, "testcases/part1_hw5_dijstra_case2.txt"))


def test_dijstra_sd_case2(dijstra_case2):
    dist = dijstra_case2.dijstra_sd("1")
    assert dist["6"] == 15
    assert dist["9"] == 22
    assert dist["10"] == 18
    assert dist["11"] == 24
    assert dist["13"] == 21


@pytest.fixture
def dijstra_case3():
    return Graph.read_input_part1_hw5(path.join(file_dir, "testcases/part1_hw5_dijstra_case3.txt"))


def test_dijstra_sd_case3(dijstra_case3):
    answer = {
        "1": 0, "2": 51, "3": 8, "4": 1, "5": 45, "6": 46, "7": 42,
        "8": 59, "9": 39, "10": 55, "11": 30, "12": 28, "13": 42, "14": 27,
        "15": 49, "16": 51, "17": 44, "18": 43, "19": 68, "20": 21, "21": 22,
        "22": 30, "23": 45, "24": 22, "25": 31, "26": 23, "27": 47, "28": 57,
        "29": 23, "30": 54, "31": 57, "32": 62, "33": 31, "34": 39, "35": 54,
        "36": 57, "37": 49, "38": 35, "39": 16, "40": 43, "41": 67, "42": 20,
        "43": 76, "44": 49, "45": 59, "46": 62, "47": 50, "48": 26, "49": 58,
        "50": 16
    }
    assert dijstra_case3.dijstra_sd("1") == answer
    assert dijstra_case3.bellman_ford_sd("1") == answer


@pytest.fixture
def apsp_case1():
    return Graph.read_input_part2_hw4(path.join(file_dir, "testcases/part2_hw4_apsp_case1.txt"))


def test_apsp_case1(apsp_case1):
    dist_pairs = apsp_case1.floyd_warshall_apsp()
    assert apsp_case1.min_dist(dist_pairs) == {("4", "1"): -2}


@pytest.fixture
def apsp_case2():
    return Graph.read_input_part2_hw4(path.join(file_dir, "testcases/part2_hw4_apsp_case2.txt"))


def test_apsp_case2(apsp_case2):
    dist_pairs = apsp_case2.floyd_warshall_apsp()
    assert apsp_case2.min_dist(dist_pairs) == {("11", "14"): -9}


@pytest.fixture
def apsp_case3():
    return Graph.read_input_part2_hw4(path.join(file_dir, "testcases/part2_hw4_apsp_case3.txt"))


def test_apsp_case3(apsp_case3):
    dist_pairs = apsp_case3.floyd_warshall_apsp()
    assert not apsp_case3.min_dist(dist_pairs)
