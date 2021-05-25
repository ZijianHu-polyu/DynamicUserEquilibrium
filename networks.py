import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

class Network:
    def __init__(self, config):
        self.nodes = None
        self.edges = None
        self.weights = None
        self.node_pos = {}
        self.network_name = config.network_name
        self.node_filepath = config.node_filepath
        self.edge_filepath = config.edge_filepath
        self.G = nx.DiGraph()

    def load(self):
        self.nodes = pd.read_csv(self.node_filepath)
        self.edges = pd.read_csv(self.edge_filepath)
        self.G = nx.from_pandas_edgelist(self.edges, "source", "target", True, create_using=nx.DiGraph)
        for each in self.nodes.values:
            self.node_pos[each[0]] = np.array(each[1:])

    def save(self):
        pass

    def draw(self):
        nx.draw(self.G, pos=self.node_pos, node_color="k", with_labels=True, node_size=400)
        nx.draw_networkx_nodes(self.G,self.node_pos, node_color='white', node_size=300)
        plt.show()

    def animation(self, colors):
        # attributes: v/c
        nx.draw(self.G, pos=self.node_pos, node_color="k", with_labels=True, node_size=400)
        vis_nodes = nx.draw_networkx_nodes(self.G, self.node_pos, node_color='white', node_size=300)
        for i, each in enumerate(colors[10:60]):
            vis_edges = nx.draw_networkx_edges(self.G, self.node_pos, edge_color=each, width=2)
            plt.savefig("images/image_%03d.jpg" % i)

        import imageio
        images = []
        for i in range(50):
            images.append(imageio.imread("images/image_%03d.jpg" % i))
        imageio.mimsave('flash.gif', images)

    def test(self):
        self.load()
        self.draw()


if __name__ == "__main__":
    a = Network()
    a.test()