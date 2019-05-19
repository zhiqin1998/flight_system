class City:
    def __init__(self, code, name, coor=(None, None), news_dicts=None, stop_dicts=None, pol_senti=None, neg_dicts=None,
                 pos_dicts=None,
                 neu_dicts=None):
        self.code = code
        self.name = name
        self.coor = coor
        self.news_dicts = news_dicts
        self.stop_dicts = stop_dicts
        self.neg_dicts = neg_dicts
        self.pos_dicts = pos_dicts
        self.neu_dicts = neu_dicts
        self.pol_senti = pol_senti

    def __repr__(self):
        s = '{}'.format(self.name)
        if self.coor.count(None) != len(self.coor):
            s = '{} -- Coordinate: ({}, {})'.format(s, self.coor[0], self.coor[1])
        if self.pol_senti is not None:
            s = '{} -- Political Sentiment: {}'.format(s, self.pol_senti)
        if self.news_dicts is not None:
            s = '{} \nNews Dicts: {}\nStop Dicts: {}\nPos Dicts: {}\nNeg Dicts: {}\nNeu Dicts: {}\n'.format(s,
                                                                                                            self.news_dicts,
                                                                                                            self.stop_dicts,
                                                                                                            self.pos_dicts,
                                                                                                            self.neg_dicts,
                                                                                                            self.neu_dicts)
            return s
