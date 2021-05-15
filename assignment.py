import networkx as nx

class BaseAssign(object):
    def __init__(self, G):
        self.G = G

    def assign(self, demand):
        return nx.shortest_path(self.G, source=demand["source"], target=demand["target"])