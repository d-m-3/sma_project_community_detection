import time
import networkx as nx

class Timer:
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        print(f"{self.message}")
        self.start = time.time()

    def __exit__(self, type, value, trace):
        time_ = time.time() - self.start
        print(f" - {time_:f} sec")


def lecture_graph():
    G = nx.Graph()
    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(1, 4)
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(4, 5)
    G.add_edge(4, 6)
    G.add_edge(5, 6)
    G.add_edge(6, 7)
    G.add_edge(7, 8)
    G.add_edge(8, 5)
    G.add_edge(5, 7)
    G.add_edge(6, 8)
    G.add_edge(7, 9)
    return G
