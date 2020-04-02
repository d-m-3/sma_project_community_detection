import networkx as nx
import matplotlib.pyplot as plt
import betweenness_centrality as bc
from tools import Timer


def empirical_evaluation(G, interval):
    """Empirical evaluation
    Plot the computation time (y-axis) given the number of nodes (x-axis)
    of subgraphs, for each interval of nodes.
    """
    X = list(range(interval, len(G.nodes) + 1, interval))
    Y_our = []
    Y_nx = []

    for i in X:
        sub_G = G.subgraph(list(G.nodes)[0:i])
        with Timer(f"Our betweenness_centrality ({i} nodes)") as t:
            bc.betweenness_centrality(sub_G)
            Y_our.append(t.get_time())
        with Timer(f"NetworkX betweenness_centrality ({i} nodes)") as t:
            nx.betweenness_centrality(sub_G)
            Y_nx.append(t.get_time())
        print("---")

    plt.figure()
    plt.title("Computing time of the function Betweenness centrality")
    plt.xlabel("Number of nodes")
    plt.ylabel("Time [s]")
    plt.plot(X, Y_our, label="Our implementation")
    plt.plot(X, Y_nx, label="NetworkX implementation")
    plt.legend()


def main():
    # Load a previously created subgraph
    sub_G = nx.read_edgelist('subgraph.gz')

    print("Comparison of the computing time of our function")
    print("and NetworkX's function (Betweenness centrality)")
    print("===")
    empirical_evaluation(sub_G, 20)


if __name__ == '__main__':
    main()