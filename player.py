class Attr(object):
    """
    A collection of player attributes with the following properties:

    attr dictionary:
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

    stats dictionary:
        G:
        AB:
        PA:
        H:
        _1B: 1B
        _2B: 2B
        _3B: 3B
        HR:
        R:
        RBI:
        BB:
        SO:
        AVG: float representing batting average (H/AB)
    """

    def __init__(self, G=0, AB=0, PA=0, H=0, _1B=0, _2B=0, _3B=0, HR=0, R=0, RBI=0,
                 BB=0, SO=0, AVG=0.0):
        """
        Return a Stats object with specified probabilities
        """
        self.stats = {}
        self.stats["G"] = G
        self.stats["AB"] = AB
        self.stats["PA"] = PA
        self.stats["H"] = H
        self.stats["1B"] = _1B
        self.stats["2B"] = _2B
        self.stats["3B"] = _3B
        self.stats["HR"] = HR
        self.stats["R"] = R
        self.stats["RBI"] = RBI
        self.stats["BB"] = BB  # (but is really BB+IBB+HBP)
        self.stats["SO"] = SO
        self.stats["AVG"] = AVG

    def get_stats_dic(self):
        return self.stats.get_stats_dic


class Player(object):
    """
    A player with the following properties:

    Attributes
        attr: Attr object
        STATS: Stats object
        name: player name
    """

    def __init__(self, name="Jon Dowd", attr=Attr(), stats=Stats()):
        """
        Return a Player object with attributes specified
        """

        #attributes
        self.attr = attr

        #statistics
        self.stats = stats

        #initialize personal info
        self.name = name

    def __str__(self):
        return self.name

    def get_stats_obj(self):
        return self.stats

    def get_attr_obj(self):
        return self.attr
