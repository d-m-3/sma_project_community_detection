#!/usr/bin/env python
import itertools
import networkx as nx
import matplotlib.pyplot as plt

from girvan_newman import girvan_newman


def analysis(G):
    print("Starting analysis")
    max_iteration_level = 4

    gn_iterator = girvan_newman(G)
    gn_iterator = itertools.islice(gn_iterator, max_iteration_level)

    communities_ = {}
    for i, communities in enumerate(gn_iterator):
        communities_[len(communities)] = communities
        print(f"Iteration {i}")
        print_infos(communities)

    return communities_


def print_infos(communities):
    """print some information regarding tuple of communities
    """
    communities = list(communities)
    communities.sort(key=lambda x: len(x))
    print(f"Number of communities : {len(communities)}")
    print(f"Size of the smallest of community : {len(communities[0])}")
    print(f"Size of the biggest of community : {len(communities[-1])}")


def vizualisation(G, communities):
    print("Starting vizualisation")
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
    G = nx.read_edgelist('subgraph.gz')
    # from tools import lecture_graph
    # G = lecture_graph()
    communities = analysis(G)
    vizualisation(G, communities)


if __name__ == '__main__':
    main()
