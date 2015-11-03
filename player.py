class Attr(object):
    """
    A collection of player attributes with the following properties:

    Attributes:
        single: float representing probability of hitting a single
        double: "" double
        triple: "" triple
        home_run: "" home run
        walk: "" walk + intentional walk (BB+IBB)
        strikeout: "" strikeout
        bbo: "" batted ball out
    """

    def __init__(self, single=.15, double=.075, triple=.025, home_run=.05,
                 walk=.05, strikeout=.2, bbo=.45):
        """
        Return an Attribute object with specified probabilities
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

    def get_attr_dic(self):
        return self.attr


class Stats(object):
    """
    A collection of player statistics with the following properties:

    STATS:
        G:
        AB:
        PA:
        H:
        B1: 1B
        B2: 2B
        B3: 3B
        HR:
        R:
        RBI:
        BB:
        SO:
        AVG: float representing batting average (H/AB)
    """

    def __init__(self, G=0, AB=0, PA=0, H=0, _1B=0, _2B=0, _3B=0, HR=0, R=0, RBI=0,
                 BB=0, IBB=0, SO=0, AVG=0.0):
        self.STATS = {}
        self.STATS["G"] = G
        self.STATS["AB"] = AB
        self.STATS["PA"] = PA
        self.STATS["H"] = H
        self.STATS["1B"] = _1B
        self.STATS["2B"] = _2B
        self.STATS["3B"] = _3B
        self.STATS["HR"] = HR
        self.STATS["R"] = R
        self.STATS["RBI"] = RBI
        self.STATS["BB"] = BB
        self.STATS["SO"] = SO
        self.STATS["AVG"] = AVG

    def get_stats_dic(self):
        return self.STATS.get_stats_dic


class Player(object):
    """
    A player with the following properties:

    Attributes
        attr: Attr object
        STATS: Stats object
        name: player name
    """

    def __init__(self, name="Jon Dowd", attr=Attr(), STATS=Stats()):
        """
        Return a Player object with attributes specified
        """

        #attributes
        self.attr = attr

        #statistics
        self.STATS = STATS

        #initialize personal info
        self.name = name

    def __str__(self):
        return self.name

    def get_stats_obj(self):
        return self.STATS

    def get_attr_obj(self):
        return self.attr
