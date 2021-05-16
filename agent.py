import copy

class Agent(object):
    # def __init__(self):
    #     self.unit = 0
    #     self.source = 0
    #     self.target = 0
    #     self.cur = 0
    #     self.time_flags = []
    #     self.route = []

    def __init__(self, unit, source, target, time_flags, cur, route):
        self.unit = unit
        self.source = source
        self.target = target
        if isinstance(time_flags, list):
            self.time_flags = copy.deepcopy(time_flags)
        else:
            self.time_flags = []
            self.time_flags.append(time_flags)
        self.cur = cur
        self.route = copy.deepcopy(route)

    def copy(self):
        return Agent(self.unit, self.source, self.target, self.time_flags, self.cur, self.route)