class Player(object):
    """
    A player with the following attributes:

    Attributes
        attr: dictionary of attributes containing (key,value) of (event,probability) of the following:
            single: float representing probability of hitting a single
            double: "" double
            triple: "" triple
            home_run: "" home run
            walk: "" walk
            strikeout: "" strikeout
            bbo: "" batted ball out
    """

    def __init__(self, single=.15, double=.075, triple=.025, home_run=.05,
                 walk=.05, strikeout=.2, bbo=.45, name="Jon Dowd"):
        """
        Return a Player object with attributes specified
        if no attributes specified, returns a game starting from the first inning
        """

        #attributes
        self.attr = {}
        self.attr["single"] = single
        self.attr["double"] = double
        self.attr["triple"] = triple
        self.attr["home_run"] = home_run
        self.attr["walk"] = walk
        self.attr["strikeout"] = strikeout
        self.attr["bbo"] = bbo

        #initialize personal info
        self.name = name

        #intialize staistics

    def get_attr(self):
        return self.attr
