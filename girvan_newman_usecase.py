#!/usr/bin/env python
import itertools
import networkx as nx
import matplotlib.pyplot as plt

from girvan_newman import girvan_newman


def analysis(G):
    print("Starting analysis...")
    max_iteration_level = 4

    gn_iterator = girvan_newman(G)
    gn_iterator = itertools.islice(gn_iterator, max_iteration_level)

    communities_ = {}
    for i, communities in enumerate(gn_iterator):
        communities_[len(communities)] = communities
        print_infos(i, communities)

    return communities_


def print_infos(iteration, communities):
    """print some information regarding tuple of communities
    """
    communities = list(communities)
    communities.sort(key=lambda x: len(x))
    header = f" Iteration {iteration}, Nb. communities : {len(communities)} "
    header = header.center(len(header) + 20, "-")
    print(header)
    for i, c in enumerate(communities):
        size = len(c)
        if size > 20:
            print(f"Community {i} sizes: {size}")
        else:
            print(f"Community {i} members: {c}")
    print("".join(len(header) * ["-"]), "\n")


def visualization(G, communities):
    """Visualize a Graph with respect of different communities levels
    each node in a same community has the same color, each node in different
    communties has a different color
    """
    print("Starting vizualisation...")
    for level, communities_level in communities.items():
        plt.figure()
        plt.title(f"Iteration: {level} ({len(communities_level)} communities)")

        # create a table with for every nodes an id
        # with respect to it's community
        colors = []
        for node in G.nodes:
            for i, community in enumerate(communities_level):
                if node in community:
                    colors.append(i)

        # draw the graph with the nodes colored in the community color and
        # the edges
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_color=colors, cmap="brg")
        nx.draw_networkx_edges(G, pos)
    plt.show()


def main():
    G = nx.read_edgelist("subgraph.gz")
    # from tools import lecture_graph
    # G = lecture_graph()
    communities = analysis(G)
    visualization(G, communities)


if __name__ == "__main__":
    main()
