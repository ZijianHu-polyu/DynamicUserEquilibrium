from demand import Demand
from loading_models.link_transmission_model import LTM
from networks.build_network import Network
from assignment import BaseAssign
from config import Config

config = Config()

if __name__ == "__main__":
    net = Network()
    demand = Demand(config)
    assign = BaseAssign()
    net.load()
    demand.load_demand()
    demand = demand.data

    model = LTM(config, net.G, demand, assign)
    model.init_graph()
    for i in range(config.timestep):
        model.update(i)
        model.load(i)

    for edge in net.G.edges:
        print(edge)
        print(net.G.edges[edge]["N_down"])