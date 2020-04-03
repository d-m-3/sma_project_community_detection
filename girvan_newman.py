#!/usr/bin/env python
import itertools
import networkx as nx
from collections import defaultdict


def girvan_newman(G):
    """Girvan Newman Algorithm"""
    G = G.copy()
    # instantiate the yield conditions
    current_number_of_communities = len(tuple(nx.connected_components(G)))
    new_number_of_communities = None

    # iterate while its still possible to remove edges
    while len(G.edges) > 0:
        edge_betweenness = edge_betweenness_centrality(G)

        # take the edge with the highest edge betweenness score
        edge_to_remove = max(edge_betweenness.keys(),
                             key=edge_betweenness.get)

        # remove this edge, unpacking because remove_edge want
        # the two endpoints of the edge
        G.remove_edge(*edge_to_remove)

        # find the communities (aka: connected components)
        communities = tuple(nx.connected_components(G))
        new_number_of_communities = len(communities)

        # if the number of communities changed
        if new_number_of_communities > current_number_of_communities:
            # set the current number of communities to the new value
            current_number_of_communities = new_number_of_communities
            # yield the communities for the current level of iteration
            yield communities


def edge_betweenness_centrality(G):
    """Calculate the edge betweeness score for every edges of the graph
    """
    counted_paths = {}
    # calculate all the shortest path for every combination of nodes
    for vi, vj in itertools.combinations(G.nodes, 2):
        # a counter for the number of paths
        nb_paths = 0
        # dictionary counting the number of path crossing through the key edge
        paths_through_edge = defaultdict(lambda: 0)
        try:
            # generate every paths for these two endpoints
            paths = nx.all_shortest_paths(G, vi, vj)
            for path in paths:
                nb_paths += 1
                # the solution is a list of node
                # the next line give us a list of edges
                edges_pathlr = list(zip(path[:-1], path[1:]))
                for l, r in edges_pathlr:
                    # the two possible directions of the edge (undirected)
                    paths_through_edge[(l, r)] += 1
                    paths_through_edge[(r, l)] += 1
        except nx.exception.NetworkXNoPath:
            pass
        counted_paths[(vi, vj)] = (nb_paths, paths_through_edge)

    # evaluate the "weekness" of the edges of the graph using
    # edge_betweeness algorithm
    edge_betweenness_dict = {edge: edge_betweenness_on_edge(
        counted_paths, edge) for edge in G.edges}

    return edge_betweenness_dict


def edge_betweenness_on_edge(counted_paths, edge):
    """Calculate the edge betweeness score for a given edge
    Need the counted_path dictionary containing the precomputed number of paths
    """
    vi, vj = edge
    sum = 0
    for (vp, vq), (nb_paths, counted_paths) in counted_paths.items():
        numerator = counted_paths[edge]
        denominator = nb_paths
        if denominator != 0:
            sum += numerator / denominator
    return sum


if __name__ == '__main__':
    print("You can import this module with : \"import girvan_newman\"")
