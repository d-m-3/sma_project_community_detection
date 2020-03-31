import networkx as nx
from girvan_newman import girvan_newman
import itertools
from tools import lecture_graph


def analysis():
    # G = nx.read_edgelist('subgraph.gz')
    # wip
    G = lecture_graph()
    gn_iterator = girvan_newman(G)

    max_iteration_level = 10

    communities_ = {}
    for communities in enumerate(itertools.islice(gn_iterator, max_iteration_level)):
        communities_[len(communities)] = communities
        print(communities)
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


def vizualisation(communities):
    pass
    # todo


if __name__ == '__main__':
    communities = analysis()
    vizualisation(communities)
