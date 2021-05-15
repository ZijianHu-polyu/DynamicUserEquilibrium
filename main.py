from demand import Demand
from loading_models.link_transmission_model import LTM
from networks.build_network import Network
from config import Config

config = Config()

if __name__ == "__main__":
    net = Network()
    demand = Demand()

    net.load()
    demand.load_demand()
    deamnd = demand.data

    model = LTM(config, net.G, demand)
    for i in range(config.timestep):
        model.load()
        model.update()