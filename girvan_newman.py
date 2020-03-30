import itertools
import random
import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman as nx_girvan_newman


def our_girvan_newman(G):
    """Girvan Newman Algorithm"""
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
                all_shortest_paths[(vj, vi)] = paths
            except nx.exception.NetworkXNoPath:
                all_shortest_paths[(vi, vj)] = []

        # evaluate the "weekness" of the edges of the graph using
        # edge_betweeness algorithm
        edge_betweenness_dict = {edge: edge_betweenness(
            all_shortest_paths, edge) for edge in G.edges}

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


def edge_betweenness(all_shortest_paths, edge):
    """Calculate the edge betweeness score for a given edge"""
    # todo
    return random.random()


def unit_tests():
    """Unit test main function"""
    # todo
    pass


def dev():
    """dev function, to remove when the module is
    finished and the unit test are written"""
    # G = nx.read_edgelist('subgraph.gz')
    G = nx.grid_graph([2, 2])

    def print_infos(communities):
        """print some information regarding tuple of communities
        """
        communities = list(communities)
        communities.sort(key=lambda x: len(x))
        print(f"Number of communities : {len(communities)}")
        print(f"Size of the smallest of community : {len(communities[0])}")
        print(f"Size of the biggest of community : {len(communities[-1])}")

    for nx_communities, our_communities in zip(nx_girvan_newman(G), our_girvan_newman(G)):
        print("Nx communities")
        print_infos(nx_communities)
        print("Our communities")
        print_infos(our_communities)
        print("")


if __name__ == '__main__':
    unit_tests()
    dev()
