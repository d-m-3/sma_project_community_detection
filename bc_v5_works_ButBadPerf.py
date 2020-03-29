#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 23:29:10 2020

@author: d3
"""

import networkx as nx
from collections import defaultdict
import time


# Compute the Betweenness Centrality for every vertex
# Returns a dictionary, with node and Betweenness Centrality for each node
def bc(G, normalize=True, directed_graph=True):
    vertices = list(G.nodes())
    bc_dict = {}
    all_paths = defaultdict(dict)

    # Get the shortest paths between all the pairs of vertices
    for vj in vertices:
        for vk in vertices:
            # all_shortest_paths return a list of lists
            #     with all the shortest paths between 2 vertices
            # all_paths is a dict (from a vertex) of dict (to all vertices),
            # containing a list of list (shortest paths)
            if vk != vj and has_path(G, vj, vk):
                all_paths[vj][vk] = [path for path in
                                       nx.all_shortest_paths(G, vj, vk)]

    # For each vertex, compute the Betweenness Centrality
    for vi in vertices:
        # Betweenness Centrality of the node
        bc_node = 0
        for vj in vertices:
            if vj != vk:
                for vk in vertices:
                    if vk != vj and vk != vi and has_path(G, vj, vk):
                        # Count the number of shortest paths that go through vi
                        sp_through_vi = 0
                        for path in all_paths[vj][vk]:
                            if vi in path[1:-1]: #path[1:-1], to exclude vj and vk
                                sp_through_vi += 1
                        # Number of shortest paths
                        nb_sp = len(all_paths[vj][vk])
                        # Betweenness Centrality of the node
                        bc_node += sp_through_vi/nb_sp
        if normalize:
            bc_dict[vi] = (bc_node * 2) / ((len(vertices) - 1)*(len(vertices) - 2))
        else:
            bc_dict[vi] = bc_node
        if directed_graph:
            bc_dict[vi] = bc_dict[vi] /2

    return bc_dict


# Test if there is a path from source to target
def has_path(G, source, target):
    try:
        nx.shortest_path(G, source, target)
    except nx.NetworkXNoPath:
        return False
    return True



# TESTS
# =====
# Load the graph, create a subgraph (subgraph.gz)
'''
print("Loading the graph...")
G = nx.read_edgelist("com-youtube.ungraph.txt")
print("Graph successfully loaded. Create subgraph and draw it.")
G_sub = G.subgraph(list(G.nodes)[0:80], create_using=nx.DiGraph())
nx.write_edgelist(G_sub, "subgraph.gz")
'''
# Load only a previously created subgraph
G_sub = nx.read_edgelist('subgraph.gz', create_using=nx.DiGraph())
nx.draw_networkx(G_sub, with_labels=True)
print("===")


# My implementation of Betweenness Centrality
start1 = time.clock()
print("My implementation of Betweenness Centrality")
print("---")
bc_dict = bc(G_sub, normalize=True, directed_graph=True)
for node, bc in bc_dict.items():
    if bc > 0:
        print("Node", node, "| Betweenness centrality :", bc)
print("===")
end1 = time.clock()


# Betweenness Centrality function from networkx
start2 = time.clock()
print("Betweenness Centrality function from networkx")
print("---")
bc_dict = nx.betweenness_centrality(G_sub)
for node, bc in bc_dict.items():
    if bc > 0:
        print("Node", node, "| Betweenness centrality :", bc)
print("===")
end2 = time.clock()


# Compare performance between my BC and nx's BC
print('My BC, computation duration: ' + str(end1 - start1))
print('BC from networkx, computation duration: ' + str(end2 - start2))