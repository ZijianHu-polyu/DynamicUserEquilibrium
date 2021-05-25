from demand import Demand
from loading_models.link_transmission_model import LTM
from networks import Network
from assignment import DUEAssign
from config import Config
import numpy as np
import matplotlib.pyplot as plt
config = Config()

if __name__ == "__main__":
    net = Network(config)
    demand = Demand(config)
    net.load()
    demand.load_demand()
    demand = demand.data

    assign = DUEAssign(config, demand)
    model = LTM(config, net.G, assign)
    model.init_graph()
    losses = []
    print("Graph %s, Nodes: %d, Edges %d" % (config.network_name, len(net.nodes), len(net.edges)))
    for iter in range(100):
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
        print("Iteration %d: Average travel time is" % iter, end="\t")
        print(travel_time)
        model.save_td_trave_time()
        model.iteration = iter + 1

        losses.append(travel_time)
        model.clear_and_reassign()  # run tdsp
    plt.plot(losses)
    plt.show()