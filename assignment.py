import heapq
import pickle
import numpy as np
import networkx as nx
INF = 999999999

class BaseAssign(object):
    def __init__(self, config, demand):
        self.demand = demand
        self.agent_list = self.demand
        self.unique_od_pairs = set(zip(self.demand["source"], self.demand["target"]))

    def generate_pathset(self, G):
        pathset = {}
        count = 0
        for each in self.unique_od_pairs:
            pathset[each] = list(nx.all_simple_paths(G, source=each[0], target=each[1]))
            count += len(pathset[each])
        return pathset, count

    def assign(self, G, iteration):
        temp = []
        for i in range(len(self.demand)):
            temp.append({tuple(nx.shortest_path(G, source=self.demand["source"][i], target=self.demand["target"][i])):
                             self.demand["unit"][i]})
        self.agent_list["route"] = temp
        print(temp)
        return self.agent_list

    def deassign(self):
        self.agent_list = self.demand


class DUEAssign(BaseAssign):
    def __init__(self, config, demand):
        super(DUEAssign, self).__init__(config, demand)
        self.travel_time_filepath = config.travel_time_filepath
        self.time_interval = config.time_interval

    def assign(self, G, iteration):
        if iteration == 0:
            temp = []
            for i in range(len(self.demand)):
                temp.append(
                    {tuple(nx.shortest_path(G, source=self.demand["source"][i], target=self.demand["target"][i])):
                         self.demand["unit"][i]})
            self.agent_list["route"] = temp
            return self.agent_list
        else: # after iteration 0
            with open(self.travel_time_filepath % (iteration - 1), "rb") as f:
                tdtt = pickle.load(f)

            for link in G.edges:
                G.edges[link]["tdtt"] = np.round(np.array(tdtt[link]) / self.time_interval)

            for i in range(len(self.demand)):
                path = tuple(self.tdsp(G, source=self.demand["source"][i], target=self.demand["target"][i], t=int(self.demand["timestep"][i]))[1])
                if path in self.agent_list["route"][i].keys():
                    pass
                else:
                    for key, value in self.agent_list["route"][i].items():
                        self.agent_list["route"][i][key] = value * (1 - 1 / np.sqrt(i+1))
                    self.agent_list["route"][i][path] = 1 / np.sqrt(i+1)
            return self.agent_list

    def tdsp(self, G, source, target, t):
        # if t > 150:
        #     return nx.shortest_path_length(G, source, target), nx.shortest_path(G, source, target)
        dis = dict((key, INF) for key in G.nodes)
        dis[source] = t
        vis = dict((key, False) for key in G.nodes)
        pq = []
        heapq.heappush(pq, [dis[source], source])
        path = dict((key, [source]) for key in G.nodes)
        while len(pq) > 0:
            v_dis, v = heapq.heappop(pq)
            if vis[v]:
                continue
            vis[v] = True
            p = path[v].copy()
            for (r, node) in G.out_edges(v):
                new_dis = int(dis[v] + G.edges[(v, node)]["tdtt"][dis[v]]) # refer to time_dependent travel time
                if new_dis < dis[node] and (not vis[node]):
                    dis[node] = new_dis
                    heapq.heappush(pq, [dis[node], node])
                    temp = p.copy()
                    temp.append(node)
                    path[node] = temp
        return dis[target], path[target]