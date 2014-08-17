# -*- coding: utf-8 -*-
"""Basic Struceture of an directed Graph

"""
from __future__ import unicode_literals
from .vertice_edge import Vertice, Edge
import os


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

    def dfs(self, start_vid):
        """Depth-first search
        Return a genertaor of vertice vids
        """
        vid_stack = [start_vid]
        visited = set()
        while vid_stack:
            current_vid = vid_stack.pop()
            if current_vid not in visited:
                yield current_vid
                visited.add(current_vid)
            else:
                continue
            for edge in self.vertices[current_vid].outgoing_edges():
                succ = edge.succ.vid
                if succ not in visited:
                    vid_stack.append(succ)

    def bfs(self, start_vid):
        """Breadth-first search
        Return a generator of vertice vids
        """
        vid_queue = [start_vid]
        visited = set()
        while vid_queue:
            current_vid = vid_queue.pop(0)
            if current_vid not in visited:
                yield current_vid
                visited.add(current_vid)
                for edge in self.vertices[current_vid].outgoing_edges():
                    succ = edge.succ.vid
                    vid_queue.append(succ)

    def finish_time_dfs(self, start_vid):
        """Depth-first search ordered according to finish time
        Return a genertaor of vertice vids
        """
        vid_stack = [start_vid]
        visited = set()
        while vid_stack:
            current_vid = vid_stack[-1]
            visited.add(current_vid)
            no_children = True
            for edge in self.vertices[current_vid].outgoing_edges():
                succ = edge.succ.vid
                if succ not in visited:
                    vid_stack.append(succ)
                    visited.add(succ)
                    no_children = False
            if no_children:
                yield vid_stack.pop()

    def kosaraju_sccs(self):
        """ Kosaraju's Self-Connected Components Algorithm
        """
        # Pass 1; Perform depth first search of the original graph starting form
        # every unvisited vertices to identify the magic ordering of vertices.
        # print("PASS1")
        vid_magic_order = []
        visited = set()
        for vid in self.vertices.keys():
            if vid in visited:
                continue
            for vid_dfs in self.finish_time_dfs(vid):
                if vid_dfs not in visited:
                    visited.add(vid_dfs)
                    vid_magic_order.append(vid_dfs)

        # Pass 2; Identify sccs using the reversed graph and the reversed
        # magic ordering of vertices. Return a generator of a list of vids
        # that belong to the same sccs.
        # print("PASS2")
        for edge in self.edges.values():
            edge.reverse()
        visited = set()
        for vid in reversed(vid_magic_order):
            if vid in visited:
                continue
            else:
                scc_vids = []
            for vid_dfs in self.dfs(vid):
                if vid_dfs not in visited:
                    visited.add(vid_dfs)
                    scc_vids.append(vid_dfs)
            yield scc_vids

    def dijstra_sd(self, start_vid):
        """Return a dictory of shortest distance from start vertice to every
        vertice using Dijstra Algorithm.
        """
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

    def bellman_ford_sd(self, start_vid):
        """Return a dictory of shortest distance from start vertice to every
        vertice using Bellman-Ford Algorighm.
        """
        n_vertices = len(self.vertices.keys())
        shortest_dist = {}
        # Initialize shortest_dist[start_vid] to be 0 and shortest_dist[other_vids] to be 1000000 (infinity)
        shortest_dist[start_vid] = 0
        for vid in self.vertices.keys():
            if vid != start_vid:
                shortest_dist[vid] = 1000000
        # Check path lengthes from 1 to n-1
        for i in range(1, n_vertices+1):
            dist_temp = {}
            for vid in self.vertices.keys():
                candidates = [shortest_dist[vid]]
                for edge in self.vertices[vid].incoming_edges():
                    pred_vid = edge.pred.vid
                    candidates.append(shortest_dist[pred_vid] + edge.weight)
                dist_temp[vid] = min(candidates)
            if dist_temp == shortest_dist:
                break
            # Check path length n to detect negative cycle
            if i == n_vertices and dist_temp != shortest_dist:
                print("Negative Cycle Detected!!!")
                shortest_dist = {}
                break
            shortest_dist = dist_temp

        return shortest_dist

    def floyd_warshall_apsp(self):
        """Floyd-Warshall All Pairs Shortest Distance Algorithm

        Returns:
            A dictionary of shortest distance pairs, such as:

                {(vid_a, vid_b): dist_ab, (vid_c, vid_d): dist_cd,...}
            If an negative cycle is detected, an empty dictionary is returned.
        """
        n_vertices = len(self.vertices.keys())
        # Initialize the dist pairs
        dist_pairs = [[0 for i in range(n_vertices+1)] for j in range(n_vertices+1)]
        edge_pairs = {}
        for edge in self.edges.values():
            pred = int(edge.pred.vid)
            succ = int(edge.succ.vid)
            edge_pairs[(pred, succ)] = edge.weight
        for vid_i in range(1, n_vertices+1):
            for vid_j in range(1, n_vertices+1):
                if (vid_i, vid_j) in edge_pairs:
                    dist_pairs[vid_i][vid_j] = edge_pairs[(vid_i, vid_j)]
                elif vid_i != vid_j:
                    dist_pairs[vid_i][vid_j] = 1000000

        # Recursion
        for vid_k in range(1, n_vertices+1):
            # progress = 1.0*vid_k/n_vertices
            # print("{}%".format(progress*100))
            dist_pairs_temp = [[0 for i in range(n_vertices+1)] for j in range(n_vertices+1)]
            for vid_i in range(1, n_vertices+1):
                for vid_j in range(1, n_vertices+1):
                    candidates = [
                        dist_pairs[vid_i][vid_j],
                        dist_pairs[vid_i][vid_k] + dist_pairs[vid_k][vid_j]
                    ]
                    dist_pairs_temp[vid_i][vid_j] = min(candidates)
                    # Check Negative Cycles
                    if vid_i == vid_j and dist_pairs_temp[vid_i][vid_j] < 0:
                        print("Negative Cycle Detected!!!")
                        return {}
            dist_pairs = dist_pairs_temp

        rt_dist_pairs = {}
        for vid_i in range(1, n_vertices+1):
            for vid_j in range(1, n_vertices+1):
                rt_dist_pairs[(str(vid_i), str(vid_j))] = dist_pairs[vid_i][vid_j]
        return rt_dist_pairs

    def min_dist(self, dist_pairs):
        """Compute the minimum distance among all pairs of shortest distances.

        Returns:
            {(vid_a, vid_b): dist}
        """
        if dist_pairs == {}:
            return None
        else:
            min_key = min(dist_pairs.keys(), key=lambda k: (dist_pairs[k], k))
            return {min_key: dist_pairs[min_key]}

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

    @classmethod
    def read_input_part1_hw4(cls, filename):
        """Reqd input file in the following format.

        [n_vertices]
        [Node_a] [Node_b]
        [Node_c] [Node_d]
        ...

        This format reads as:
        There are total of n_vertices in this graph. For this graph,
        there exists one edge originated from a to b, c to d and so on...
        """
        g = cls()
        file = open(filename, "r")
        n_vertices = int(file.readline())
        for vid in range(1, n_vertices+1):
            g.add_vertice(str(vid))
        eid = 1
        for line in file:
            pred_vid, succ_vid = line.split()
            g.add_edge(str(eid), pred_vid, succ_vid)
            eid += 1
        file.close()
        return g

    @classmethod
    def read_input_part1_hw5(cls, filename):
        """Read input file in the following format.

        [node_1] [node_a],[cost_a] [node_b],[cost_b]...
        ...

        This reade as: there exist one edge originated from node_1 to node_a
        with cost_a, to node_b with cost_b,....
        """
        g = cls()
        n_vertices = os.popen("wc -l {}".format(filename)).read().split()[0]
        n_vertices = int(n_vertices)
        for vid in range(1, n_vertices+1):
            g.add_vertice(str(vid))
        eid = 1
        file = open(filename, "r")
        for line in file:
            info = line.split()
            pred_vid = info[0]
            for edge_info in info[1:]:
                succ_vid, weight = edge_info.split(",")
                g.add_edge(str(eid), pred_vid, succ_vid, int(weight))
                eid += 1
        file.close()
        return g

    @classmethod
    def read_input_part2_hw2_q1(cls, filename):
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

    @classmethod
    def read_input_part2_hw4(cls, filename):
        """Read input file in the following format.

        [number_of_nodes] [number_of_edges]
        [edge 1 node 1] [edge 1 node 2] [edge 1 cost]
        [edge 2 node 1] [edge 2 node 2] [edge 2 cost]
        ...

        """
        g = cls()
        file = open(filename, "r")
        n_vertices, n_edges = file.readline().split()
        n_vertices = int(n_vertices)
        n_edges = int(n_edges)
        for vid in range(1, n_vertices+1):
            g.add_vertice(str(vid))
        eid = 1
        for line in file:
            pred_vid, succ_vid, weight = line.split()
            g.add_edge(str(eid), pred_vid, succ_vid, int(weight))
            eid += 1
        file.close()
        return g

    @classmethod
    def read_input_part2_hw6(cls, filename):
        """Reqd input file of a 2-set problem in the following format

        [n_variables]
        [var_a] [var_b]
        [var_c] [var_d]
        ...

        The file format is as follows. In each instance, the number of variables
        and the number of clauses is the same, and this number is specified
        on the first line of the file. Each subsequent line specifies a clause
        via its two literals, with a number denoting the variable and a "-" sign
        denoting logical "not".

        For example, the second line of the first data file is "-16808 75250",
        which indicates the clause ¬x16808 ∨ x75250.

        Return the graph representation of such 2-set problem.

        """
        g = cls()
        file = open(filename, "r")
        n_vertices = int(file.readline())
        for vid in range(1, n_vertices+1):
            g.add_vertice(str(vid))
            g.add_vertice(str(-vid))
        edge_pairs = set()
        for line in file:
            pred_vid, succ_vid = line.split()
            edge_pairs.add((str(-int(pred_vid)), succ_vid))
            edge_pairs.add((str(-int(succ_vid)), pred_vid))
        file.close()
        eid = 1
        for pair in edge_pairs:
            pred_vid, succ_vid = pair
            g.add_edge(str(eid), pred_vid, succ_vid)
            eid += 1
        for vid in g.vertices.keys():
            if len(g.vertices[vid].edges) == 0:
                del g.vertices[vid]
        return g

