import unittest
import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman as nx_girvan_newman
from girvan_newman import girvan_newman as our_girvan_newman
from tools import lecture_graph


def test_girvan_newman():
    """Unit test main function"""
    G = nx.grid_graph([4, 4])
    #todo


def test_edge_betweeness():
    G = lecture_graph()
    #todo
