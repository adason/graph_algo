"""Test graph class

"""
from __future__ import unicode_literals
import pytest
from graph_algo.graph import Graph


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
    return Graph.read_input_part1_hw5("testcases/dijstra_part1_hw5_case1.txt")


@pytest.fixture
def dijstra_case2():
    return Graph.read_input_part1_hw5("testcases/dijstra_part1_hw5_case2.txt")


@pytest.fixture
def dijstra_case3():
    return Graph.read_input_part1_hw5("testcases/dijstra_part1_hw5_case3.txt")


def test_dijstra_sd_case1(dijstra_case1):
    assert dijstra_case1.dijstra_sd("1") == {"1": 0, "2": 1, "3": 2, "4": 1, "7": 7, "6": 6, "5": 4}


def test_dijstra_sd_case2(dijstra_case2):
    dist = dijstra_case2.dijstra_sd("1")
    assert dist["6"] == 15
    assert dist["9"] == 22
    assert dist["10"] == 18
    assert dist["11"] == 24
    assert dist["13"] == 21


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
