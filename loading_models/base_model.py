class BaseModel:
    def __init__(self, G):
        self.G = G
        self.jam_density = 0.2 # vehicle per meter
        self.duration = -1 # the longest loading time
        self.time_interval = -1
        self.timestep = 0
        self.total_travel_time = []
        for edge in self.G.edges:
            self.G.edges[edge]["buffer"] = []

    def init_graph(self):
        pass

    def fd(self, link): # triangular fundamental diagram
        res = []
        for each in link["density"]:
            if each > self.jam_density:
                res.append(0)
            elif each > link["critical_density"]:
                res.append(link["backward_speed"] * (self.jam_density - each))
            else:
                res.append(link["forward_speed"] * each)
        return res

    def fd_speed_density(self, link): # triangular fundamental diagram
        res = []
        for each in link["density"]:
            if each > self.jam_density:
                res.append(0)
            elif each > link["critical_density"]:
                res.append(link["backward_speed"] * (self.jam_density - each) / each)
            else:
                res.append(link["forward_speed"])
        return res

    def get_supply(self, t, link):
        pass

    def get_demand(self, t, link):
        pass

    def update(self, t):
        pass