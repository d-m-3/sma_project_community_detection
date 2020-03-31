import itertools
import networkx as nx
from tools import Timer
from collections import defaultdict


def girvan_newman(G):
    """Girvan Newman Algorithm"""
    G = G.copy()
    # instantiate the yield conditions
    current_number_of_communities = len(tuple(nx.connected_components(G)))
    new_number_of_communities = None

    # iterate while its still possible to remove edges
    while len(G.edges) > 0:
        # calculate all the shortest path for every combination of nodes
        # needed for the edge_betweeness computation

        all_shortest_paths = {}
        for vi, vj in itertools.combinations(G.nodes, 2):
            try:
                paths = list(nx.all_shortest_paths(G, vi, vj))
                all_shortest_paths[(vi, vj)] = paths
            except nx.exception.NetworkXNoPath:
                all_shortest_paths[(vi, vj)] = []

        # compute dictionary needed by edge betweenness
        counted_paths = count_paths(all_shortest_paths, G.edges)

        # evaluate the "weekness" of the edges of the graph using
        # edge_betweeness algorithm
        edge_betweenness_dict = {edge: edge_betweenness(
            counted_paths, edge) for edge in G.edges}

        # take the edge with the highest edge_betweenness score
        edge_to_remove = max(edge_betweenness_dict.keys(),
                             key=edge_betweenness_dict.get)

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

            yield tuple(nx.connected_components(G))


def count_paths(all_shortest_paths, edges):
    """Return a dictionary containing for every shortest path for all
    combination of endpoints:
    - The number of paths
    - For each edge : the number of path involved
    """
    count_paths = {}
    for (start, end), paths in all_shortest_paths.items():
        nb_paths = len(paths)
        counted_paths = defaultdict(lambda: 0)
        for path in paths:
            edges_pathlr = list(zip(path[:-1], path[1:]))
            for l, r in edges_pathlr:
                counted_paths[(l, r)] += 1
                counted_paths[(r, l)] += 1
        count_paths[(start, end)] = (nb_paths, counted_paths)
    return count_paths


def edge_betweenness(counted_paths, edge):
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
