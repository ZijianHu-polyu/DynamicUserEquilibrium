import networkx as nx

class BaseAssign(object):
    def __init__(self):
        pass

    def assign(self, G, demand, cur):
        return nx.shortest_path(G, source=demand["source"][cur], target=demand["target"][cur])