from collections import deque
import numpy as np
from agent import Agent
from loading_models.base_model import BaseModel

class LTM(BaseModel):
    def __init__(self, config, G, demands, routes):
        super(LTM, self).__init__(G)
        self.duration = config.duration
        self.time_interval = config.time_interval
        self.timestep = int(self.duration / self.time_interval)
        self.demands = demands
        self.route = routes

    def init_graph(self):
        for edge in self.G.edges:
            self.G.edges[edge]["N_up"] = np.zeros(self.timestep)
            self.G.edges[edge]["N_down"] = np.zeros(self.timestep)
            self.G.edges[edge]["Q_in"] = np.zeros(self.timestep)
            self.G.edges[edge]["Q_out"] = np.zeros(self.timestep)
            self.G.edges[edge]["forward_time"] = self.G.edges[edge]["fft"]
            self.G.edges[edge]["backward_time"] = 3 * self.G.edges[edge]["fft"]
            self.G.edges[edge]["forward_speed"] = int(self.G.edges[edge]["L"] / self.G.edges[edge]["forward_time"])
            self.G.edges[edge]["backward_speed"] = int(self.G.edges[edge]["L"] / self.G.edges[edge]["backward_time"])
            self.G.edges[edge]["queue"] = deque()
            self.G.edges[edge]["supply"] = 0
            self.G.edges[edge]["demand"] = 0

    def get_demand(self, t, link):
        t_prime = t + 1 - self.G.edges[link]["forward_time"]
        if t_prime < 0:
            return 0
        else:
            return min((self.G.edges[link]["N_up"][t_prime] - self.G.edges[link]["N_down"][t_prime]), link["capcity"])
    
    def get_supply(self, t, link):
        t_prime = t + 1 - self.G.edges[link]["backward_time"]
        if t_prime < 0:
            return 0
        else:
            return min((self.G.edges[link]["N_down"][t_prime] - self.G.edges[link]["N_up"][t_prime] + self.G.edges[link]["length"] * self.jam_density), link["capcity"])

    def load(self, t):
        cur = 0
        while self.demands["timestep"][cur] == t:
            route = route.assign(self.demands[cur])
            self.G.edges[(route[0], route[1])]["queue"].append(Agent(
                self.demands["unit"][cur],
                self.demands["source"][cur],
                self.demands["target"][cur],
                0,
                route
            ))
            cur += 1
            
    def pre_update(self, t):
        for link in self.G.edges:
            self.G.edges[link]["demand"] = self.get_demand(t, self.G.edges[link])
            self.G.edges[link]["supply"] = self.get_supply(t, self.G.edges[link])

    def update(self, t):
        self.pre_update(t)
        for node in self.G.nodes:
            print(node)
            in_links = self.G.in_edges(node)
            for in_link in in_links:
                while len(self.G.edges[in_link]["queue"]) >= 0 or self.G.edges[in_link]["demand"] >= 0:
                    top_agent = self.G.edges[in_link]["queue"][0]
                    next_edge = self.G.edges[(top_agent[top_agent.cur + 1], top_agent[top_agent.cur + 2])]
                    if top_agent.unit <= next_edge["supply"]:
                        top_agent.cur += 1
                        self.G.edges[(top_agent[top_agent.cur], top_agent[top_agent.cur + 1])]["queue"].append(top_agent)
                        self.G.edges[(top_agent[top_agent.cur], top_agent[top_agent.cur + 1])]["supply"] -= top_agent.unit
                        self.G.edges[in_link]["queue"].popleft()
                        self.G.edges[in_link]["demand"] -= top_agent.unit

                    elif next_edge["supply"] == 0:
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