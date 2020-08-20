class Asset:

    # Constructor
    def __init__(self, id, name):
        self.id = id
        self.name = name

    # ToString Method
    def __str__(self):
        return 'Asset {self.id}'.format(self=self)
