#!/usr/bin/env python
import itertools
import networkx as nx
import matplotlib.pyplot as plt

from networkx.algorithms.community.centrality import girvan_newman as nx_girvan_newman
from girvan_newman import girvan_newman as our_girvan_newman

from networkx.algorithms.centrality import edge_betweenness_centrality as nx_edge_betweenness_centrality
from girvan_newman import edge_betweenness_centrality as our_edge_betweenness_centrality

from tools import Timer


def benchmark_girvan_newman(G):
    print("Starting benchmark_girvan_newman...")
    max_iteration_level = 10

    Y_our = []
    Y_nx = []

    our_it = our_girvan_newman(G)
    nx_it = nx_girvan_newman(G)

    our_it = itertools.islice(our_it, max_iteration_level)
    nx_it = itertools.islice(nx_it, max_iteration_level)

    i = 0
    while True:
        try:
            with Timer(f"Starting iteration {i} on our girvan newman") as t:
                next(our_it)
                Y_our.append(t.get_time())
            with Timer(f"Starting iteration {i} on nx girvan newman") as t:
                next(nx_it)
                Y_nx.append(t.get_time())
        except StopIteration:
            break
        i += 1

    X = list(range(len(Y_our)))
    plt.figure()
    plt.title("Time over iteration for executing girvan newman")
    plt.xlabel("Iteration level []")
    plt.ylabel("Time [s]")
    plt.plot(X, Y_our, label="Our implementation")
    plt.plot(X, Y_nx, label="Networkx implementation")
    plt.legend()
    plt.savefig("benchmark_girvan_newman.png")

    Y_our_cumulative = get_cumulative_array(Y_our)
    Y_nx_cumulative = get_cumulative_array(Y_nx)

    plt.figure()
    plt.title("Cumulative time over iteration for executing girvan newman")
    plt.xlabel("Iteration level []")
    plt.ylabel("Time [s]")
    plt.plot(X, Y_our_cumulative, label="Our implementation")
    plt.plot(X, Y_nx_cumulative, label="Networkx implementation")
    plt.legend()
    plt.savefig("benchmark_girvan_newman_cumulative.png")


def benchmark_edge_betweenness_centrality(G):
    print("Starting benchmark_edge_betweenness_centrality...")

    X = list(range(0, len(G.nodes), 5))
    Y_our = []
    Y_nx = []

    for i in X:
        sub_G = G.subgraph(list(G.nodes)[0:i])
        with Timer("Starting our edge_betweenness_centrality") as t:
            our_edge_betweenness_centrality(sub_G)
            Y_our.append(t.get_time())
        with Timer("Starting nx edge_betweenness_centrality") as t:
            nx_edge_betweenness_centrality(sub_G)
            Y_nx.append(t.get_time())

    plt.figure()
    plt.title("Time over graph size for executing edge_betweenness_centrality")
    plt.xlabel("Iteration level []")
    plt.ylabel("Time [s]")
    plt.plot(X, Y_our, label="Our implementation")
    plt.plot(X, Y_nx, label="Networkx implementation")
    plt.legend()
    plt.savefig("benchmark_edge_betweenness_centrality.png")


def get_cumulative_array(a):
    sum = 0
    b = []
    for i in a:
        b.append(i + sum)
        sum += i
    return b


def main():
    G = nx.read_edgelist("subgraph.gz")
    # from tools import lecture_graph
    # G = lecture_graph()
    benchmark_girvan_newman(G)
    benchmark_edge_betweenness_centrality(G)

    plt.show()


if __name__ == "__main__":
    main()
