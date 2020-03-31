import itertools
import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman as nx_girvan_newman
from tools import Timer
from collections import defaultdict


def our_girvan_newman(G):
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


def unit_tests():
    """Unit test main function"""
    # todo
    pass


def dev():
    """dev function, to remove when the module is
    finished and the unit test are written"""
    G = nx.read_edgelist('subgraph.gz')

    # G = nx.grid_graph([10, 10])

    # G = nx.Graph()
    # G.add_edge(1, 2)
    # G.add_edge(1, 3)
    # G.add_edge(1, 4)
    # G.add_edge(2, 3)
    # G.add_edge(3, 4)
    # G.add_edge(4, 5)
    # G.add_edge(4, 6)
    # G.add_edge(5, 6)
    # G.add_edge(6, 7)
    # G.add_edge(7, 8)
    # G.add_edge(8, 5)
    # G.add_edge(5, 7)
    # G.add_edge(6, 8)
    # G.add_edge(7, 9)

    print(len(G.edges))

    def print_infos(communities):
        """print some information regarding tuple of communities
        """
        communities = list(communities)
        communities.sort(key=lambda x: len(x))
        print(f"Number of communities : {len(communities)}")
        print(f"Size of the smallest of community : {len(communities[0])}")
        print(f"Size of the biggest of community : {len(communities[-1])}")

    nx_it = nx_girvan_newman(G)
    our_it = our_girvan_newman(G)

    while True:
        try:
            with Timer("Networkx Pass"):
                nx_communities = next(nx_it)
        except StopIteration:
            break
        print("Nx communities")
        print_infos(nx_communities)

        print("")

        try:
            with Timer("Our Pass"):
                our_communities = next(our_it)
        except StopIteration:
            break
        print("Our communities")
        print_infos(our_communities)

        print("")
        print("")


if __name__ == '__main__':
    unit_tests()
    dev()
