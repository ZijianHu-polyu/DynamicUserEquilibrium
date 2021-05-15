import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

class Network:
    def __init__(self, name_prefix="networks/Nguyen"):
        self.nodes = None
        self.edges = None
        self.weights = None
        self.node_pos = {}
        self.network_name = name_prefix
        self.G = nx.DiGraph()

    def load(self):
        self.nodes = pd.read_csv(self.network_name + "_nodes.csv")
        self.edges = pd.read_csv(self.network_name + "_edges.csv")
        self.G = nx.from_pandas_edgelist(self.edges, "source", "target", True, create_using=nx.DiGraph)
        for each in self.nodes.values:
            self.node_pos[each[0]] = np.array(each[1:])

    def save(self):
        pass
    
    def draw(self):
        nx.draw(self.G, pos=self.node_pos, node_color="k", with_labels=True, node_size=400)
        nx.draw_networkx_nodes(self.G,self.node_pos, node_color='white', node_size=300)
        plt.show()

    def test(self):
        self.load()
        self.draw()


if __name__ == "__main__":
    a = Network()
    a.test()