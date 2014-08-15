# -*- coding: utf-8 -*-
"""Test graph class

"""
from __future__ import unicode_literals
import pytest
import textwrap
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


def test_graph_print(g):
    correct_answer = """\
        vid: 1; out_eids: 1; in_eids: 3
        vid: 2; out_eids: 2; in_eids: 1
        vid: 3; out_eids: 3; in_eids: 2
        ==========
        eid: 1; vids: 1 2; weight: 2
        eid: 2; vids: 2 3; weight: 1
        eid: 3; vids: 3 1; weight: 3
    """
    assert "{}".format(g) == textwrap.dedent(correct_answer)


@pytest.fixture
def g2():
    g2 = Graph()
    g2.add_vertice("1")
    g2.add_vertice("2")
    g2.add_vertice("3")
    g2.add_vertice("4")
    g2.add_vertice("5")
    g2.add_vertice("6")
    g2.add_edge("1", "1", "2")
    g2.add_edge("2", "1", "3")
    g2.add_edge("3", "3", "5")
    g2.add_edge("4", "5", "4")
    g2.add_edge("5", "2", "5")
    g2.add_edge("6", "3", "2")
    g2.add_edge("7", "2", "6")
    return g2


def test_dfs(g2):
    assert list(g2.dfs("1")) == ["1", "3", "2", "6", "5", "4"]


def test_bfs(g2):
    assert list(g2.bfs("1")) == ["1", "2", "3", "5", "6", "4"]
