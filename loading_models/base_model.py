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
        if link["density"] > self.jam_density:
            return 0
        elif link["density"] > link["critical_density"]:
            return link["backward_speed"] * (self.jam_density - link["density"])
        else:
            return link["foward_speed"] * link["density"]

    def get_supply(self, t, link):
        pass

    def get_demand(self, t, link):
        pass

    def update(self, t):
        pass