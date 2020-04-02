import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import time


def betweenness_centrality(G, normalize=True, shortest_paths_time=False):
    """Computes the Betweenness centrality for every vertex.
    Returns a dictionary, with node and Betweenness centrality for each node.
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
    Returns a dict (from a vertex) of dict (to all vertices),
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


def load_graph_and_create_subgraph(number_of_nodes, filename):
    """Loads the graph and creates a subgraph.
    """
    print("Loading the graph...")
    G = nx.read_edgelist("com-youtube.ungraph.txt")
    print("Graph successfully loaded.")
    print(f"Create the subgraph '{filename}' of {number_of_nodes} nodes.")
    G_sub = G.subgraph(list(G.nodes)[0:number_of_nodes])
    nx.write_edgelist(G_sub, filename)
    return G_sub


def draw_graph(G, k_top_users_list):
    """Draws the graph and highlights the k top users.
    """
    pos = nx.spring_layout(G) # Force directed algorithm
    color_dict = {}
    for top_user in k_top_users_list:
        color_dict[top_user] = 'red'
    color_list = [color_dict.get(node, 'blue') for node in G.nodes()]
    plt.figure(1,figsize=(12,12))
    nx.draw(G, pos, with_labels = True, node_size = 60, font_size = 8,
            node_color=color_list, edge_color = 'g', width = 1, alpha = 0.7)
    return pos # Dictionary of positions keyed by node


def plot_empirical_evaluation(G, interval):
    """Empirical evaluation
    Plots the computation time (y-axis) given the number of nodes (x-axis)
    of subgraphs, for each interval of nodes.
    """
    graph_values = {}
    for nodes in range(interval, G.number_of_nodes(), interval):
        Gi = G.subgraph(list(G.nodes)[0:nodes])
        start = time.time()
        betweenness_centrality(Gi)
        end = time.time()
        duration = end - start
        graph_values[nodes] = duration
    return graph_values


# Show the correctness, get the top users and draw the graph
if __name__ == '__main__':

    # Load a previously created subgraph
    G_sub = nx.read_edgelist('subgraph.gz')

    # Define the number of top users (k) we are interested to show
    k = 4

    # Show the correctness of the implementation, compared to nx's function
    # ---------------------------------------------------------------------
    # Our implementation of Betweenness centrality
    print("Our implementation of Betweenness centrality \n---")
    bc_dict = betweenness_centrality(G_sub, normalize=True,
                                     shortest_paths_time = False)
    for node, bc in bc_dict.items():
        if bc > 0:
            print("Node", node, "| Betweenness centrality :", bc)
    print("---")
    k_top_users_list = sorted(bc_dict, key=bc_dict.get, reverse=True)[:k]
    print(f"The {k} top users are : {k_top_users_list}")
    print("===")

    # Betweenness centrality function from networkx
    print("Betweenness centrality function from NetworkX \n---")
    bc_dict_nx = nx.betweenness_centrality(G_sub)
    for node, bc in bc_dict_nx.items():
        if bc > 0:
            print("Node", node, "| Betweenness centrality :", bc)
    print("---")
    k_top_users_list_nx = sorted(bc_dict, key=bc_dict_nx.get, reverse=True)[:k]
    print(f"The {k} top users are : {k_top_users_list_nx}")
    print("===")

    # Draw the graph and highlight the k top users, in red
    pos = draw_graph(G_sub, k_top_users_list)