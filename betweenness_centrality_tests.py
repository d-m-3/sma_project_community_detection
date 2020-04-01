import unittest
import networkx as nx
import betweenness_centrality as bc
from tools import lecture_graph


class TestBetweennessCentrality(unittest.TestCase):

    Gs = [lecture_graph(), nx.florentine_families_graph(),
          nx.karate_club_graph()]

    def test_compare_our_betweenness_centrality_with_networkx(self):
        """Compare the output of our betweenness centrality algorithm with networkx's
        """
        for G in TestBetweennessCentrality.Gs:
            our_bc = bc.betweenness_centrality(G)
            nx_bc = nx.betweenness_centrality(G)

            # DEBUG
            print("our bc", our_bc, "\n---")
            print("nx bc ", nx_bc, "\n---")

            try:
                self.assertAlmostEqual(our_bc, nx_bc)
            except StopIteration:
                break


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBetweennessCentrality)
    unittest.TextTestRunner(verbosity=2).run(suite)