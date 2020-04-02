import networkx as nx
import matplotlib.pyplot as plt
import time
import betweenness_centrality as bc


if __name__ == '__main__':
    # Load the graph, create a subgraph
    #G_eval = bc.load_graph_and_create_subgraph(120, "subgraph_eval.gz")

    # Load a previously created subgraph
    G_eval = nx.read_edgelist('subgraph_eval.gz')

    # Computation time of our implementation of Betweenness centrality
    start1 = time.time()
    bc_dict = bc.betweenness_centrality(G_eval)
    end1 = time.time()

    # Computation time of Betweenness centrality function from NetworkX
    start2 = time.time()
    bc_dict_nx = nx.betweenness_centrality(G_eval)
    end2 = time.time()

    # Compare performance between my BC and nx's BC
    print("Evaluation of our function Betweenness centrality, for 120 nodes")
    print("===")
    print("Computation time, our function:", str(end1 - start1), "s")
    print("Computation time, function from NetworkX:", str(end2 - start2), "s")
    print("===")

    # Empirical evaluation's plot
    graph_values = bc.plot_empirical_evaluation(G_eval, 20)
    plt.plot(*zip(*sorted(graph_values.items())))
    plt.figure(1)
    plt.title("Computation time")
    plt.ylabel("Time [s]")
    plt.xlabel("Number of nodes")
    plt.show()