
class Agent(object):
    def __init__(self):
        self.unit = 0
        self.source = 0
        self.target = 0
        self.cur = 0
        self.route = []

    def __init__(self, unit, source, target, cur, route):
        self.unit = unit
        self.source = source
        self.target = target
        self.cur = cur
        self.route = route

    def copy(self):
        return Agent(self.unit, self.source, self.target, self.cur, self.route)