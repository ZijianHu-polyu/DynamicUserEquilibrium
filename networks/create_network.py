import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

edges_list = [(1, 5), (1, 12), (4, 5), (4, 9), (5, 6), (5, 9), (6, 7), (6, 10), (7, 8), (7, 11), (8, 2), (9, 10), (9, 13), (10, 11), (11, 2), (11, 3), (12, 6), (12, 8), (13, 3)]
pos = {
    1: np.array([1, 3]),
    2: np.array([4, 1]),
    3: np.array([3, 0]),
    4: np.array([0, 2]),
    5: np.array([1, 2]),
    6: np.array([2, 2]),
    7: np.array([3, 2]),
    8: np.array([4, 2]),
    9: np.array([1, 1]),
    10: np.array([2, 1]),
    11: np.array([3, 1]),
    12: np.array([2, 3]),
    13: np.array([2, 0])
    }

edges = pd.DataFrame(columns=["source", "target", "length", "forward_speed", "backward_speed", "capacity"])
edges["source"] = [each[0] for each in edges_list]
edges["target"] = [each[1] for each in edges_list]
edges["capacity"] = np.ones(len(edges_list)) * 0.8333
edges["length"] = [1500, 3000, 3000, 4500, 3000, 1500, 3000, 1500, 3000, 1500, 1500, 3000, 4500, 3000, 3000, 1500, 1500, 1500, 9000, 3000]
edges["travel_time"] = []
edges["forward_speed"] = np.ones_like(len(edges_list))
edges["backward_speed"] = np.zeros(len(edges_list))

edges.to_csv("Nguyen_edges.csv", index=False)

nodes = pd.DataFrame(columns=["id", "pos_x", "pos_y"])
nodes["id"] = [i for i in range(1, 14)]
nodes["pos_x"] = [pos[i][0] for i in range(1, 14)]
nodes["pos_y"] = [pos[i][1] for i in range(1, 14)]
nodes.to_csv("Nguyen_nodes.csv", index=False)