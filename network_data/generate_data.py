import os
import numpy as np
import networkx as nx
import pandas as pd
from scipy.io import loadmat
import matplotlib.pyplot as plt
import sys
import warnings
    
network_name = "Anaheim"
def load_data():
    od_data = loadmat(os.path.join(network_name, "OD_info.mat"))
    detail_data = loadmat(os.path.join(network_name, "networks.mat"))
    return od_data, detail_data

def save_demand(od_data, detail_data):
    source = detail_data["source"][0][0][0]
    sink = detail_data["sink"][0][0][0]
    od_pairs_index = od_data["OD_set"]
    od_pairs = []
    for each in od_pairs_index:
        od_pairs.append([source[each[0] - 1][0], sink[each[1] - 1][0]])
    od_pairs_length = len(od_pairs)
    od_pairs = np.array(od_pairs)
    od_pairs = np.concatenate([od_pairs for _ in range(30)], axis=0)
    timestep = [np.ones([od_pairs_length, 1]) * (i+10) for i in range(30)]
    timestep = np.concatenate(timestep, axis=0)
    units = np.ones_like(timestep) * 0.2
    od_pairs = np.c_[timestep, od_pairs, units]
    od_pairs = pd.DataFrame(od_pairs, columns=["timestep", "source", "target", "unit"])
    od_pairs.to_csv(os.path.join(network_name, "demands.csv"), index=False)

def save_edge(detail_data):
    if np.shape(np.array(detail_data["linkData"]))[1] == 6:
        edges = pd.DataFrame(np.array(detail_data["linkData"]), columns=["source", "target", "capacity", "length", "fft", "unknown"])
    elif np.shape(np.array(detail_data["linkData"]))[1] == 5:
        edges = pd.DataFrame(np.array(detail_data["linkData"]), columns=["source", "target", "capacity", "length", "fft"])
    edges.to_csv(os.path.join(network_name, "edges.csv"), index=False)
    
    return edges

def save_node(detail_data):
    nodes = np.expand_dims(np.arange(1, detail_data["node"][0][0][0][0][0] + 1, dtype=np.int32), 1)
    if len(detail_data["node"].dtype) < 4:
        warnings.warn("The matlab file do not contains the location of nodes. You can setup by your own or let them be empty", UserWarning, stacklevel=2)
        pos_x = np.zeros_like(nodes)
        pos_y = np.zeros_like(nodes)
    else:
        pos_x = np.array(detail_data["node"][0][0][1])
        pos_y = np.array(detail_data["node"][0][0][2])
    
    nodes = np.c_[nodes, pos_x, pos_y]
    nodes = pd.DataFrame(nodes, columns=["id", "pos_x", "pos_y"])
    nodes.to_csv(os.path.join(network_name, "nodes.csv"), index=False)
    return nodes

def plot_network(nodes, edges, isdirected=False):
    G = nx.DiGraph()
    if not isdirected:
        G = nx.Graph()
    
    G.add_edges_from(np.c_[edges["source"], edges["target"]])
    pos = {}
    for i in range(len(nodes)):
        pos[nodes["id"][i]] = np.array([nodes["pos_x"][i], nodes["pos_y"][i]])
    nx.draw_networkx(G, pos=pos)
    plt.show()

if __name__ == "__main__":
    od_data, detail_data = load_data()
    save_demand(od_data, detail_data)
    edges = save_edge(detail_data)
    nodes = save_node(detail_data)
    plot_network(nodes, edges)