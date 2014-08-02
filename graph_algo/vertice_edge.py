# -*- coding: utf-8 -*-
"""Vertices and edges classes for graph

"""
from __future__ import unicode_literals


class Vertice(object):

    def __init__(self, vid):
        self.vid = vid
        self.edges = set()

    def attach_edge(self, edge):
        self.edges.add(edge)

    def outgoing_edges(self):
        return [e for e in self.edges if e.pred.vid == self.vid]

    def incoming_edges(self):
        return [e for e in self.edges if e.succ.vid == self.vid]

    def __str__(self):
        out_eids = [e.eid for e in self.outgoing_edges()]
        out_eids.sort()
        in_eids = [e.eid for e in self.incoming_edges()]
        in_eids.sort()
        rtn_str = "vid: {0}; out_eids: {1}; in_eids: {2}"
        return rtn_str.format(self.vid, " ".join(out_eids), " ".join(in_eids))


class Edge(object):

    def __init__(self, eid, weight=1):
        self.eid = eid
        self.weight = weight
        self.pred = None
        self.succ = None

    def attach_pred(self, vertice):
        self.pred = vertice

    def attach_succ(self, vertice):
        self.succ = vertice

    def vertices(self):
        return [self.pred, self.succ]

    def __str__(self):
        rtn_str = "eid: {0}; vids: {1} {2}; weight: {3}"
        return rtn_str.format(self.eid, self.pred.vid, self.succ.vid, self.weight)
