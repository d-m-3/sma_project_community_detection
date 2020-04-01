import networkx as nx
import matplotlib.pyplot as plt
import time
import betweenness_centrality as bc


# Load the graph, create a subgraph
#G_sub = bc.load_graph_and_create_subgraph(100, "subgraph_eval.gz")

# Load a previously created subgraph
G_sub = nx.read_edgelist('subgraph_eval.gz', create_using=nx.DiGraph())

# Computation time of our implementation of Betweenness centrality
start1 = time.clock()
bc_dict = bc.betweenness_centrality(G_sub, normalize=True, directed_graph=True,
                                    shortest_paths_time = False)
end1 = time.clock()

# Computation time of Betweenness centrality function from NetworkX
start2 = time.clock()
bc_dict = nx.betweenness_centrality(G_sub)
end2 = time.clock()

# Compare performance between my BC and nx's BC
print("Evaluation")
print("===")
print('Computation time, our Betweenness centrality function: ', str(end1 - start1))
print('Computation time, function from NetworkX: ', str(end2 - start2))

# Empirical evaluation's plot
graph_values = bc.plot_empirical_evaluation(G_sub, 20)
plt.plot(*zip(*sorted(graph_values.items())))
plt.figure(1)
plt.show()