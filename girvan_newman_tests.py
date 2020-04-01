import unittest
import networkx as nx

from networkx.algorithms.community.centrality import girvan_newman as nx_girvan_newman
from girvan_newman import girvan_newman as our_girvan_newman

from networkx.algorithms.centrality import edge_betweenness_centrality as nx_edge_betweenness_centrality
from girvan_newman import edge_betweenness_centrality as our_edge_betweenness_centrality

from tools import lecture_graph


class TestGirvanNewman(unittest.TestCase):

    Gs = [lecture_graph(), nx.florentine_families_graph(),
          nx.karate_club_graph()]

    def test_compare_our_girvan_newman_with_networkx(self):
        """Compare the output of our girvan newman algorithm with netwrokx's

        The output might not by the same in some cases (non-exhaustive list):
            - if the graph has two pair of edges with the same edge betweeness
            (happens a lot with symetric graphs)
        """
        for G in TestGirvanNewman.Gs:
            # create iterators
            our_it = our_girvan_newman(G)
            nx_it = nx_girvan_newman(G)

            # for every level of communities
            while True:
                try:
                    our_communities = next(our_it)
                    nx_communities = next(nx_it)
                    self.assertEqual(our_communities, nx_communities)
                except StopIteration:
                    break

    def test_compare_our_edge_betweenness_centrality_with_networkx(self):
        """Compare the output of our edge betweenness centrality algorithm with netwrokx's
        """
        for G in TestGirvanNewman.Gs:
            our_edge_betweenness = our_edge_betweenness_centrality(G)
            # we can only handle non normalized edge betweeness
            # (because for gw it's doesnt matter)
            nx_edge_betweenness = nx_edge_betweenness_centrality(
                G, normalized=False)

            side_by_side = zip(our_edge_betweenness.items(),
                               nx_edge_betweenness.items())

            for (our_pair, our_value), (nx_pair, nx_value) in side_by_side:
                self.assertEqual(our_pair, nx_pair)
                self.assertAlmostEqual(our_value, nx_value, places=6)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGirvanNewman)
    unittest.TextTestRunner(verbosity=2).run(suite)
