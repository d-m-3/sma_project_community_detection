import networkx as nx
import betweenness_centrality as bc
import matplotlib.pyplot as plt


def load_graph_and_create_subgraph(number_of_nodes, filename):
    """Load the YouTube graph and creates a subgraph.
    """
    print("Loading the graph...")
    G = nx.read_edgelist("com-youtube.ungraph.txt")
    print("Graph successfully loaded.")
    print(f"Create the subgraph '{filename}' of {number_of_nodes} nodes.")
    sub_G = G.subgraph(list(G.nodes)[0:number_of_nodes])
    nx.write_edgelist(sub_G, filename)
    return sub_G


def draw_graph(G, k_top_users_list):
    """Draw the graph and highlights the k top users.
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


def get_top_k_users(bc_dict, k):
    """Return a list of the top k users with highest Betweenness centrality
    """
    return sorted(bc_dict, key=bc_dict.get, reverse=True)[:k]


def print_betweenness_centrality_and_top_k_users(bc_dict, k):
    """Print betweenness centrality for all vertices and print a list
    of the top k users.
    """
    for node, b in bc_dict.items():
        if b > 0:
            print("Node", node, "| Betweenness centrality :", b)
    print("---")
    print(f"The top {k} users are : {get_top_k_users(bc_dict, k)}")
    print("===")


def main():
    """Show the correctness, get the top users and draw the graph.
    The top users are shown in red.
    """
    # Load the graph, create a subgraph
    #G_sub = load_graph_and_create_subgraph(100, "subgraph.gz")

    # Load a previously created subgraph
    sub_G = nx.read_edgelist('subgraph.gz')

    # Define the number of top users (k) we are interested to show
    k = 4

    # Show the correctness of the implementation, compared to nx's function
    print("Our implementation of Betweenness centrality \n---")
    bc_dict = bc.betweenness_centrality(sub_G)
    print_betweenness_centrality_and_top_k_users(bc_dict, k)
    print("Implementation of Betweenness centrality from NetworkX \n---")
    bc_dict_nx = nx.betweenness_centrality(sub_G)
    print_betweenness_centrality_and_top_k_users(bc_dict_nx, k)

    # Draw the graph and highlight the top k users, in red
    draw_graph(sub_G, get_top_k_users(bc_dict, k))


if __name__ == '__main__':
    main()