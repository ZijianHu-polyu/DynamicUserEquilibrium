import networkx as nx

class BaseAssign(object):
    def __init__(self, demand):
        self.demand = demand
        self.agent_list = self.demand

    def assign(self, G):
        temp = []
        for i in range(len(self.demand)):
            temp.append(nx.shortest_path(G, source=self.demand["source"][i], target=self.demand["target"][i]))
        self.agent_list["route"] = temp
        return self.agent_list


class DUEAssign(BaseAssign):
    def __init__(self, demand):
        super(DUEAssign, self).__init__(demand)
        self.unique_od_pairs = set(zip(self.demand["source"], self.demand["target"]))
        print(self.unique_od_pairs)