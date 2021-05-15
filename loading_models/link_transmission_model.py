from collections import deque
from matplotlib.pyplot import contour
import numpy as np
from agent import Agent
from loading_models.base_model import BaseModel
import math

# TODO: Add buffer after each update.
class LTM(BaseModel):
    def __init__(self, config, G, demands, routes):
        super(LTM, self).__init__(G)
        self.duration = config.duration
        self.time_interval = config.time_interval
        self.timestep = config.timestep
        self.demands = demands
        self.routes = routes
        self.load_cur = 0

    def init_graph(self):
        for edge in self.G.edges:
            self.G.edges[edge]["N_up"] = np.zeros(self.timestep + 1)
            self.G.edges[edge]["N_down"] = np.zeros(self.timestep + 1)
            self.G.edges[edge]["Q_in"] = np.zeros(self.timestep + 1)
            self.G.edges[edge]["Q_out"] = np.zeros(self.timestep + 1)
            self.G.edges[edge]["forward_time"] = self.G.edges[edge]["fft"]
            self.G.edges[edge]["backward_time"] = 3 * self.G.edges[edge]["fft"]
            self.G.edges[edge]["forward_speed"] = int(self.G.edges[edge]["length"] / self.G.edges[edge]["forward_time"])
            self.G.edges[edge]["backward_speed"] = int(self.G.edges[edge]["length"] / self.G.edges[edge]["backward_time"])
            self.G.edges[edge]["queue"] = deque()
            self.G.edges[edge]["supply"] = 0
            self.G.edges[edge]["demand"] = 0

    def get_demand(self, t, link):
        t_prime = t - max(math.ceil(link["forward_time"] / self.time_interval), 1) + 1
        if t_prime < 0:
            return 0
        else:
            return min((link["N_up"][t_prime] - link["N_down"][t]), link["capacity"])
    
    def get_supply(self, t, link):
        t_prime = t - max(math.ceil(link["backward_time"] / self.time_interval), 1) + 1
        if t_prime < 0:
            return 0
        else:
            return min((link["N_down"][t_prime] - link["N_up"][t] + link["length"] * self.jam_density), link["capacity"])

    def load(self, t):
        if self.load_cur >= len(self.demands["timestep"]):
            return
        while self.demands["timestep"][self.load_cur] == t:
            route = self.routes.assign(self.G, self.demands, self.load_cur)
            self.G.edges[(route[0], route[1])]["queue"].append(Agent(
                self.demands["unit"][self.load_cur],
                self.demands["source"][self.load_cur],
                self.demands["target"][self.load_cur],
                0,
                route
            ))
            self.G.edges[(route[0], route[1])]["Q_in"][t] += self.demands["unit"][self.load_cur]
            self.G.edges[(route[0], route[1])]["N_up"][t + 1] += self.demands["unit"][self.load_cur]
            self.load_cur += 1
            if self.load_cur >= len(self.demands["timestep"]):
                break
            
    def pre_update(self, t):
        for link in self.G.edges:

            self.G.edges[link]["demand"] = self.get_demand(t, self.G.edges[link])
            self.G.edges[link]["supply"] = self.get_supply(t, self.G.edges[link])
            self.G.edges[link]["N_up"][t + 1] += self.G.edges[link]["N_up"][t]
            self.G.edges[link]["N_down"][t + 1] += self.G.edges[link]["N_down"][t]

    def update(self, t):
        self.pre_update(t)
        for node in self.G.nodes:
            in_links = self.G.in_edges(node)
            for in_link in in_links:
                while len(self.G.edges[in_link]["queue"]) > 0 and self.G.edges[in_link]["demand"] >= 0:
                    top_agent = self.G.edges[in_link]["queue"][0]
                    if top_agent.cur != len(top_agent.route) - 2:
                        next_edge = self.G.edges[(top_agent.route[top_agent.cur + 1], top_agent.route[top_agent.cur + 2])]
                    
                        if top_agent.unit <= next_edge["supply"]:
                            top_agent.cur += 1
                            self.G.edges[(top_agent.route[top_agent.cur], top_agent.route[top_agent.cur + 1])]["queue"].append(top_agent)
                            self.G.edges[(top_agent.route[top_agent.cur], top_agent.route[top_agent.cur + 1])]["supply"] -= top_agent.unit
                            self.G.edges[in_link]["queue"].popleft()
                            self.G.edges[in_link]["demand"] -= top_agent.unit
                            self.G.edges[in_link]["Q_out"][t] += top_agent.unit
                            self.G.edges[in_link]["N_down"][t + 1] += top_agent.unit
                            self.G.edges[(top_agent.route[top_agent.cur], top_agent.route[top_agent.cur + 1])]["Q_in"][t] += top_agent.unit
                            self.G.edges[(top_agent.route[top_agent.cur], top_agent.route[top_agent.cur + 1])]["N_up"][t + 1] += top_agent.unit
                        elif next_edge["supply"] <= 0:
                            break
                        # still have vacancy for agent
                        else:
                            pre_agent = top_agent.copy()
                            pre_agent.unit = top_agent.unit - next_edge["supply"]
                            pre_agent.cur += 1
                            self.G.edges[in_link]["queue"][0].unit -= pre_agent.unit
                            self.G.edges[(pre_agent[pre_agent.cur], pre_agent[pre_agent.cur + 1])]["queue"].append(pre_agent)
                            self.G.edges[(pre_agent[pre_agent.cur], pre_agent[pre_agent.cur + 1])]["supply"] = 0
                            self.G.edges[in_link]["demand"] -= pre_agent.unit
                            self.G.edges[in_link]["Q_out"][t] += pre_agent.unit
                            self.G.edges[in_link]["N_down"][t + 1] += pre_agent.unit
                            self.G.edges[(top_agent.route[top_agent.cur], top_agent.route[top_agent.cur + 1])]["Q_in"][t] += pre_agent.unit
                            self.G.edges[(top_agent.route[top_agent.cur], top_agent.route[top_agent.cur + 1])]["N_up"][t + 1] += pre_agent.unit

                    else: # sink link
                        self.G.edges[(top_agent.route[top_agent.cur], top_agent.route[top_agent.cur + 1])]["supply"] -= top_agent.unit
                        self.G.edges[in_link]["demand"] -= top_agent.unit
                        self.G.edges[in_link]["Q_out"][t] += top_agent.unit
                        self.G.edges[in_link]["N_down"][t + 1] += top_agent.unit
                        self.G.edges[in_link]["queue"].popleft()