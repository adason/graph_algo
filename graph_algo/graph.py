# -*- coding: utf-8 -*-
"""Basic Struceture of an Undirected Graph

"""
from __future__ import unicode_literals
from .vertice_edge import Vertice, Edge


class Graph(object):

    def __init__(self):
        self.vertices = {}
        self.edges = {}

    def add_vertice(self, vid):
        self.vertices[vid] = Vertice(vid)

    def add_edge(self, eid, pred_vid, succ_vid, weight=1):
        self.edges[eid] = Edge(eid, weight)
        self.vertices[pred_vid].attach_edge(self.edges[eid])
        self.vertices[succ_vid].attach_edge(self.edges[eid])
        self.edges[eid].attach_pred(self.vertices[pred_vid])
        self.edges[eid].attach_succ(self.vertices[succ_vid])

    def __str__(self):
        str_rep = ""
        for vid in sorted(self.vertices.keys()):
            str_rep += "{}\n".format(self.vertices[vid])
        str_rep += "==========\n"
        for eid in sorted(self.edges.keys()):
            str_rep += "{}\n".format(self.edges[eid])
        return str_rep

    def shortest_dist(self, start_vid):
        """Return a dictory of distance from start vertice to every vertice"""
        shortest_dist = {}  # Keep track of distance of vertices visited
        temp_dist = {}  # Keep track of unvisited vertice temperart distance
        temp_dist[start_vid] = 0
        for vid in self.vertices.keys():
            if vid != start_vid:
                temp_dist[vid] = 1000000

        while temp_dist:
            current_vid = min(temp_dist, key=temp_dist.get)
            shortest_dist[current_vid] = temp_dist[current_vid]
            del temp_dist[current_vid]
            for edge in self.vertices[current_vid].outgoing_edges():
                update_vid = edge.succ.vid
                update_dist = shortest_dist[current_vid] + edge.weight
                if temp_dist.get(update_vid) and temp_dist.get(update_vid) > update_dist:
                    temp_dist[update_vid] = update_dist

        return shortest_dist

    @classmethod
    def read_input_q1(cls, filename):
        """Read input file in the following format.

        [number_of_nodes]
        [edge 1 node 1] [edge 1 node 2] [edge 1 cost]
        [edge 2 node 1] [edge 2 node 2] [edge 2 cost]
        ...

        """
        g = cls()
        file = open(filename, "r")
        n_vertices = int(file.readline())
        for vid in range(1, n_vertices+1):
            g.add_vertice(str(vid))
        eid = 1
        for line in file:
            pred_vid, succ_vid, weight = line.split()
            g.add_edge(str(eid), pred_vid, succ_vid, int(weight))
            eid += 1
        file.close()
        return g
