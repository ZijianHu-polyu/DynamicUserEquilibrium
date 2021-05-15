from loading_models.base_model import BaseModel

class LKModel(BaseModel):
    def __init__(self, G):
        super(LKModel, self).__init__(G)
        pass

    def get_demand(self, link):
        if link["density"] < link["critical_density"]:
            return self.fd(link["density"])
        else:
            return self.fd(link["capacity"])
    
    def get_supply(self, link):
        if link["density"] < link["critical_density"]:
            return self.fd(link["capcity"])
        else:
            return self.fd(link["density"])

    def update(self):
        for node in self.G:
            pass