
class Config(object):
    def __init__(self):
        self.jam_density = 0.2
        self.duration = 2
        self.time_interval = 1
        self.timestep = int(self.duration * 3600 / self.time_interval)
        self.network_name = "Nguyen"
        self.node_filepath = "network_data/%s/nodes.csv" % self.network_name
        self.edge_filepath = "network_data/%s/edges.csv" % self.network_name
        self.demand_filepath = "network_data/%s/demands.csv" % self.network_name
        self.travel_time_filepath = "outputs/link_travel_time_%03d.pkl"
