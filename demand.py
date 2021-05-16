import pandas as pd
from pandas._config import config
from config import Config

config = Config()

class Demand(object):
    def __init__(self, config):
        self.filepath = config.demand_filepath
        self.timestep = config.timestep
        self.data = []

    def load_demand(self):
        self.data = pd.read_csv(self.filepath)
        self.data["unit"] *= 10

    def generate_demand(self):
        self.data = []
        od_pairs = [(1, 2), (4, 2), (1, 3), (4, 3)]
        for i in range(100):
            if i < 10 or i > 40:
                continue
            for each in od_pairs:
                self.data.append([i, each[0], each[1], 0.2])
        self.data = pd.DataFrame(self.data, columns=["timestep", "source", "target", "unit"])


    def save_demand(self):
        self.data.to_csv(self.filepath, index=False)


if __name__ == "__main__":
    a = Demand(config)
    a.generate_demand()
    a.save_demand()