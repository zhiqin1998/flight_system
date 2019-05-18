class City:
    def __init__(self, code, name, coor=(None, None), pol_senti=None):
        self.code = code
        self.name = name
        self.coor = coor
        self.pol_senti = pol_senti

    def __repr__(self):
        s = '{}'.format(self.name)
        if self.coor.count(None) != len(self.coor):
            s = '{} -- Coordinate: ({}, {})'.format(s, self.coor[0], self.coor[1])
        if self.pol_senti is not None:
            s = '{} -- Political Sentiment: {}'.format(s, self.pol_senti)
        return s
