# -*- coding: utf-8 -*-
"""Test graph class

"""
from __future__ import unicode_literals
import pytest
import textwrap
from graph_algo.graph import Graph


@pytest.fixture
def g1():
    g = Graph()
    g.add_vertice("1")
    g.add_vertice("2")
    g.add_vertice("3")
    g.add_edge("1", "1", "2", 2)
    g.add_edge("2", "2", "3", 1)
    g.add_edge("3", "3", "1", 3)
    return g


def test_g1_print(g1):
    correct_answer = """\
        vid: 1; out_eids: 1; in_eids: 3
        vid: 2; out_eids: 2; in_eids: 1
        vid: 3; out_eids: 3; in_eids: 2
        ==========
        eid: 1; vids: 1 2; weight: 2
        eid: 2; vids: 2 3; weight: 1
        eid: 3; vids: 3 1; weight: 3
    """
    assert "{}".format(g1) == textwrap.dedent(correct_answer)

def test_shortest_dist(g1):
    assert g1.shortest_dist("1") == {"1": 0, "2": 2, "3": 3}
