
class Config(object):
    def __init__(self):
        self.jam_density = 0.2
        self.duration = 10
        self.time_interval = 180
        self.timestep = int(self.duration * 3600 / self.time_interval)
        self.demand_filepath = "networks/Nguyen_demands.csv"
