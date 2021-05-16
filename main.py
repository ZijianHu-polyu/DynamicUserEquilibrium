from demand import Demand
from loading_models.link_transmission_model import LTM
from networks.build_network import Network
from assignment import BaseAssign, DUEAssign
from config import Config
import numpy as np
config = Config()

if __name__ == "__main__":
    net = Network()
    demand = Demand(config)
    net.load()
    demand.load_demand()
    demand = demand.data

    assign = DUEAssign(demand)
    model = LTM(config, net.G, assign)
    model.init_graph()
    for i in range(config.timestep):
        model.pre_update(i)
        model.update(i)
        model.pro_update()
        model.load(i)

    # for edge in net.G.edges:
    #     print(edge)
    #     print(net.G.edges[edge]["N_up"][100:])
    #     print(net.G.edges[edge]["N_down"][100:])
    colors = model.set_vac()
    # net.animation(colors)
    travel_time = np.array(model.total_travel_time).T
    travel_time = np.sum(travel_time[0] * travel_time[1]) / np.sum(travel_time[1])
    print("Average travel time is")
    print(travel_time)