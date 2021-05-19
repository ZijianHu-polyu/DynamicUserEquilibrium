
class Config(object):
    def __init__(self):
        self.jam_density = 0.2
        self.duration = 1
        self.time_interval = 5
        self.timestep = int(self.duration * 3600 / self.time_interval)
        self.demand_filepath = "networks/Nguyen_demands.csv"
        self.travel_time_filepath = "outputs/link_travel_time_%03d.pkl"
