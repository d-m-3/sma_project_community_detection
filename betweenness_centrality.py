#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 23:29:10 2020

@author: d3
"""

import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import time


# Compute the Betweenness centrality for every vertex
# Returns a dictionary, with node and Betweenness centrality for each node
def betweenness_centrality(G, normalize=True, directed_graph=True,
                           shortest_paths_time=False):
    vertices = list(G.nodes())
    bc_dict = {}
    all_paths = defaultdict(dict)

    if shortest_paths_time:
        start = time.clock()

    # Get the shortest paths between all the pairs of vertices
    for vj in vertices:
        for vk in vertices:
            # all_shortest_paths return a list of lists
            #     with all the shortest paths between 2 vertices
            # all_paths is a dict (from a vertex) of dict (to all vertices),
            # containing a list of list (shortest paths)
            if vk != vj and nx.has_path(G, vj, vk):
                all_paths[vj][vk] = [path for path in
                                       nx.all_shortest_paths(G, vj, vk)]

    # Display the computation time to get all the shortest paths
    if shortest_paths_time:
        print("Time to compute all the shortest paths :",
              time.clock() - start, "\n---")

    # For each vertex, compute the Betweenness centrality
    for vi in vertices:
        # Betweenness centrality of the node
        bc_node = 0
        for vj in vertices:
            if vj != vi:
                for vk in vertices:
                    if vk != vj and vk != vi and nx.has_path(G, vj, vk):
                        # Count the number of shortest paths that go through vi
                        sp_through_vi = 0
                        for path in all_paths[vj][vk]:
                            if vi in path[1:-1]: #path[1:-1], to exclude vj and vk
                                sp_through_vi += 1
                        # Number of shortest paths
                        nb_sp = len(all_paths[vj][vk])
                        # Betweenness centrality of the node
                        bc_node += sp_through_vi/nb_sp
        if normalize:
            bc_dict[vi] = (bc_node * 2) / ((len(vertices) - 1)*(len(vertices) - 2))
        else:
            bc_dict[vi] = bc_node
        if directed_graph:
            bc_dict[vi] = bc_dict[vi] /2

    return bc_dict


# Function to draw the graph and highlight the k top users
def draw_graph(G, k_top_users_list):
    pos = nx.spring_layout(G)
    val_map = {}
    for top_user in k_top_users_list:
        val_map[top_user] = 'red'
    values = [val_map.get(node, 'blue') for node in G.nodes()]
    plt.figure(1,figsize=(12,12))
    nx.draw(G, pos, with_labels = True, node_size = 60, font_size = 8,
            node_color=values, edge_color = 'g', width = 1, alpha = 0.7)
    return pos



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
print("===")


# Define the number of top users (k) we are interested to show
k = 4


# My implementation of Betweenness centrality
start1 = time.clock()
print("My implementation of Betweenness centrality")
print("---")
bc_dict = betweenness_centrality(G_sub, normalize=True, directed_graph=True,
                                 shortest_paths_time = False)
for node, bc in bc_dict.items():
    if bc > 0:
        print("Node", node, "| Betweenness centrality :", bc)
end1 = time.clock()
print("---")
k_top_users_list = sorted(bc_dict, key=bc_dict.get, reverse=True)[:k]
print(f"The {k} top users are : {k_top_users_list}")
print("===")


# Betweenness centrality function from networkx
start2 = time.clock()
print("Betweenness centrality function from networkx")
print("---")
bc_dict = nx.betweenness_centrality(G_sub)
for node, bc in bc_dict.items():
    if bc > 0:
        print("Node", node, "| Betweenness centrality :", bc)
end2 = time.clock()
print("---")
print(f"The {k} top users are : {sorted(bc_dict, key=bc_dict.get, reverse=True)[:k]}")
print("===")


# Compare performance between my BC and nx's BC
print('My Betweenness centrality, computation time: ' + str(end1 - start1))
print('Betweenness centrality from networkx, computation time: ' + str(end2 - start2))


# Draw the graph and highlight the k top users
pos = draw_graph(G_sub, k_top_users_list)
plt.show()




'''
Remarks for the report
At first, I had computed the shortest paths between two vertices in the main loop (where I compute Betweenness
centrality). But the algorithm was slow. I obtained a notable improvement, about 400% quicker, when I computed
first all the shortest paths first, in a separate loop.
For test purposes, I have tested the computation time for computing the shortest paths only.
For 80 nodes, it's 0.17s in average, and the total computation time for the Betweenness
centrality function is about 4.34s.
In comparison, the computation time of all the shortest paths is negligible, as it represent
about 3.9%.
'''