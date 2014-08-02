# -*- coding: utf-8 -*-
"""Algorithms for Minimum Spanning Trees

"""
from __future__ import unicode_literals
from .graph import Graph


class MST(Graph):

    def mst_prim(self, start_vid="1"):
        """Use Prim's Algorighm to find the minimum spanning tree"""
        visited_nodes = set([start_vid])
        crossing_edges = set()
        for edge in self.vertices[start_vid].edges:
            crossing_edges.add(edge.eid)

        mst = set()
        while crossing_edges:
            cheapest_eid = min(crossing_edges,
                               key=lambda eid: (self.edges.get(eid).weight, eid))
            mst.add(cheapest_eid)
            if self.edges[cheapest_eid].pred.vid in visited_nodes and self.edges[cheapest_eid].succ.vid in visited_nodes:
                raise("BUG!!! Both nodes attached to edge {} are visited.".format(cheapest_eid))
            if self.edges[cheapest_eid].pred.vid in visited_nodes:
                succ_vid = self.edges[cheapest_eid].succ.vid
            elif self.edges[cheapest_eid].succ.vid in visited_nodes:
                succ_vid = self.edges[cheapest_eid].pred.vid
            else:
                raise("BUG!!! Edge {} is not a crossing edge.".format(cheapest_eid))
            visited_nodes.add(succ_vid)

            # Maintain crossing edges
            for edge in self.vertices[succ_vid].edges:
                crossing_edges.add(edge.eid)
            for eid in list(crossing_edges):
                if self.edges[eid].pred.vid in visited_nodes and self.edges[eid].succ.vid in visited_nodes:
                    crossing_edges.remove(eid)

        return mst

    def mst_kruskal(self):
        """Use Kruskal's Algorighm to find the minimum spanning tree"""
        sorted_edges = sorted(self.edges.keys(),
                              key=lambda eid: (self.edges.get(eid).weight, eid))
        # Keep track of the lead_node vid and the rank
        # This will be modified during union-find with path compression,
        # as well as the merge step.
        leader_info = {vid: {"leader": vid, "rank": 0} for vid in self.vertices.keys()}

        mst = set()
        for eid in sorted_edges:
            pred_vid = self.edges[eid].pred.vid
            succ_vid = self.edges[eid].succ.vid
            pred_leader_vid = self._find_leader(leader_info, pred_vid)
            succ_leader_vid = self._find_leader(leader_info, succ_vid)

            # Merge two groups
            if pred_leader_vid != succ_leader_vid:
                mst.add(eid)
                self._merge_groups(leader_info, pred_leader_vid, succ_leader_vid)

        return mst

    def mst_cost(self, mst_eids):
        return sum([self.edges.get(eid).weight for eid in mst_eids])

    def _find_leader(self, leader_info, vid):
        """Given the vid, find it's leader node and perform path compression"""
        # Traverse up the leader tree to find the real leader
        leader_vid = leader_info[vid]["leader"]
        while leader_info[leader_vid]["leader"] != leader_vid:
            leader_vid = leader_info[leader_vid]["leader"]
        # Path compression
        while leader_info[vid]["leader"] != leader_vid:
            parent_vid = leader_info[vid]["leader"]
            leader_info[vid]["leader"] = leader_vid
            vid = parent_vid

        return leader_vid

    def _merge_groups(self, leader_info, pred_leader_vid, succ_leader_vid):
        """Merge the groups using leder node"""
        if leader_info[pred_leader_vid]["rank"] > leader_info[succ_leader_vid]["rank"]:
            leader_info[succ_leader_vid]["leader"] = pred_leader_vid
        elif leader_info[pred_leader_vid]["rank"] < leader_info[succ_leader_vid]["rank"]:
            leader_info[pred_leader_vid]["leader"] = succ_leader_vid
        else:  # When both group leaders have the same rank
            leader_info[succ_leader_vid]["leader"] = pred_leader_vid
            leader_info[pred_leader_vid]["rank"] += 1

    def clustering(self, k=4):
        """Compute a max-spacing k-clustering.

        Args:
            k (int): The number of desired clusters.

        Returns:
            A tuple with two objects: (cluster, maximum_spacing), where cluster
            is represented as a dict and maximum_spacing is an itetger.
            For example:

            cluster = {"1": set("1", "2"), "3": set("3", "4"), "5": set("5", "6")}
            indicates that cluster 1 with leater "1" has tow vertices "1", "2",
            and cluster 2 with leader "3" has two vertices "3", "4"...

            maximum_spacing = 4 represents the maximum value among all spacings
            between these clusters.

        """
        sorted_edges = sorted(self.edges.keys(),
                              key=lambda eid: (self.edges.get(eid).weight, eid))

        # Keep track of the lead_node vid and its rank
        # This will be modified during union-find step with path compression and the merge step.
        leader_info = {vid: {"leader": vid, "rank": 0} for vid in self.vertices.keys()}

        # Keep track of the number of groups
        n_groups = len(self.vertices)
        for eid in sorted_edges:
            pred_vid = self.edges[eid].pred.vid
            succ_vid = self.edges[eid].succ.vid
            pred_leader_vid = self._find_leader(leader_info, pred_vid)
            succ_leader_vid = self._find_leader(leader_info, succ_vid)

            # Merge two groups
            if pred_leader_vid != succ_leader_vid:
                if n_groups > k:
                    self._merge_groups(leader_info, pred_leader_vid, succ_leader_vid)
                    n_groups -= 1
                # When we have n_groups == k and right before the next merge
                # that will make n_groups < k
                else:
                    clusters = self._identify_clusters(leader_info)
                    spacing = self.edges.get(eid).weight
                    break

        return (clusters, spacing)

    def _identify_clusters(self, leader_info):
        """Deduce the custer structure from leader_info.

        This method expects a path compressed leader_info.
        Otherwise this method might be slow.

        """
        clusters = {}
        for vid in leader_info.keys():
            leader = self._find_leader(leader_info, vid)
            if leader in clusters:
                clusters[leader].add(vid)
            else:
                clusters[leader] = set([vid])

        return clusters

