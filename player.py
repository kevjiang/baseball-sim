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
                 BB=0, SO=0, AVG=0.0, SLG=0.0, OBP=0.0):
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
        self.stats["AVG"] = AVG  # will only be recalculated through recalculate_avg function internally
        self.stats["SLG"] = SLG  # will only be recalculated through recalculate_slg function internally
        self.stats["OBP"] = OBP  # will only be recalculated through recalculate_obp function internally

    def get_stats_dic(self):
        return self.stats

    # set stats dic at key to value
    # returns final value stored
    # note will always recalculate AVG based on new information
    def set_stats_dic(self, key, value):
        self.stats[key] = value
        self.recalculate_all()
        return self.stats[key]

    # increment stats dic at key by incr
    # returns final value stored
    # note will always recalculate AVG based on new information
    def incr_stats_dic(self, key, incr):
        self.stats[key] += incr
        self.recalculate_all()
        return self.stats[key]

    # recalculates stored average rounded to 3 decimal places
    def recalculate_avg(self):
        if self.stats["AB"] != 0:
            self.stats["AVG"] = round(self.stats["H"] / float(self.stats["AB"]), 3)

    # recalculates stored SLG rounded to 3 decimal places
    def recalculate_slg(self):
        if self.stats["AB"] != 0:
            numerator = self.stats["1B"] + 2 * self.stats["2B"] + \
                3 * self.stats["3B"] + 4 * self.stats["HR"]
            self.stats["SLG"] = round(numerator / float(self.stats["AB"]), 3)

    # recalculates stored OBP rounded to
    # real formula is H+BB+HBP/AB+BB+HBP+SF, which isn't used here yet...
    def recalculate_obp(self):
        denominator = self.stats["AB"] + self.stats["BB"]
        if denominator != 0:
            numerator = self.stats["H"] + self.stats["BB"]
            self.stats["OBP"] = round(numerator / float(denominator), 3)

    # calls all recalculations necessary after stat update
    def recalculate_all(self):
        self.recalculate_avg()
        self.recalculate_slg()
        self.recalculate_obp()

    #need a function to reset all stats to 0


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

        # attributes
        self.attr = attr

        # statistics
        self.stats = stats

        # initialize personal info
        self.name = name

    def __str__(self):
        return self.name

    def get_stats_obj(self):
        return self.stats

    def get_attr_obj(self):
        return self.attr

    def get_name(self):
        return self.name

    # sets stat object at key to value
    # returns final value stored
    def set_stats_obj(self, key, value):
        return self.stats.set_stats_dic(key, value)

    # increments stat object at key by incr
    # returns final value stored
    def incr_stats_obj(self, key, incr):
        return self.stats.incr_stats_dic(key, incr)
