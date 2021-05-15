
class Config(object):
    def __init__(self):
        self.duration = 5
        self.time_interval = 180
        self.timestep = int(self.duration * 3600 / self.time_interval)
        self.demand_filepath = "networks/Nguyen_demands.csv"
