# -*- coding: utf-8 -*-
"""Test vertice and edge class

"""
from __future__ import unicode_literals
import pytest
from graph_algo.vertice_edge import Vertice, Edge


class SimGraph(object):
    def __init__(self):
        self.v1 = Vertice("1")
        self.v2 = Vertice("2")
        self.e1 = Edge("1")
        self.v1.attach_edge(self.e1)
        self.v2.attach_edge(self.e1)
        self.e1.attach_pred(self.v1)
        self.e1.attach_succ(self.v2)


@pytest.fixture
def sg():
    return SimGraph()


def test_v1_outgoing(sg):
    assert list(sg.v1.outgoing_edges()) == [sg.e1]


def test_v2_incoming(sg):
    assert list(sg.v2.incoming_edges()) == [sg.e1]


def test_v1_print(sg):
    assert "{}".format(sg.v1) == "vid: 1; out_eids: 1; in_eids: "


def test_e1_print(sg):
    assert "{}".format(sg.e1) == "eid: 1; vids: 1 2; weight: 1"
