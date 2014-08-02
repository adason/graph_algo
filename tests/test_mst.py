# -*- coding: utf-8 -*-
"""Test the MST methods in graph_algo"""


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


def test_mst_prim(g):
    assert g.mst_prim() == set(["1", "2"])


def test_mst_kruskal(g):
    assert g.mst_kruskal() == set(["1", "2"])


def test_clustring(g):
    clusters, maximum_spacing = g.clustering(2)
    assert clusters == {"1": set(["1"]), "2": set(["2", "3"])}
    assert maximum_spacing == 2
