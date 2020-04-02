import networkx as nx
from collections import defaultdict
import time


def betweenness_centrality(G, normalize=True, shortest_paths_time=False):
    """Compute the Betweenness centrality for every vertex.
    Return a dictionary, with node and Betweenness centrality for each node.
    """
    vertices = list(G.nodes())
    bc_dict = {}

    # Get all the shortest paths between all the pairs of vertices
    all_paths = get_all_paths_for_all_pairs(G, vertices, shortest_paths_time)

    # For each vertex, compute the Betweenness centrality
    for vi in vertices:
        # Betweenness centrality of the node
        bc_node = 0
        for i, vj in enumerate(vertices[:-1]): # Exclude last, because vk = vj + 1
            for vk in vertices[i+1:]:
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

    return bc_dict


def get_all_paths_for_all_pairs(G, vertices, shortest_paths_time):
    """Get all the shortest paths between all the pairs of vertices.
    Return a dict (from a vertex) of dict (to all vertices),
    containing a list of lists (with all the shortest paths between 2 vertices).
    """
    # defaultdict has a default value if a key has not been set yet
    all_paths = defaultdict(dict)

    if shortest_paths_time:
        start = time.clock()

    for i, vj in enumerate(vertices[:-1]): # Exclude last, because vk = vj + 1
        for vk in vertices[i+1:]:
            # all_shortest_paths returns a list of lists
            #     with all the shortest paths between 2 vertices
            all_paths[vj][vk] = [path for path in
                     nx.all_shortest_paths(G, vj, vk)]

    # Display the computation time to get all the shortest paths
    if shortest_paths_time:
        print("Time to compute all the shortest paths :",
              time.clock() - start, "\n---")

    return all_paths


if __name__ == '__main__':
    print("You can import this module with : \"import betweenness_centrality\"")