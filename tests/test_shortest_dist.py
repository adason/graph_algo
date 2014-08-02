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
