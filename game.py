import random

events = {
    "single": 1,
    "double": 2,
    "triple": 3,
    "home_run": 4,
    "walk": 5,
    "strikeout": 6,
    "bbo": 7
}

events2 = {
    1: "single",
    2: "double",
    3: "triple",
    4: "home_run",
    5: "walk",
    6: "strikeout",
    7: "bbo"
}


# given dictionary of weighted choices, returns random weighted choice
def weighted_choice(choices):
    total = sum(v for k, v in choices.items())
    r = random.uniform(0, total)
    upto = 0
    for k, v in choices.items():
        if upto + v > r:
            return k
        upto += v
    assert False, "weighted_choice: Shouldn't get here"


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
                 walk=.05, strikeout=.2, bbo=.45):
        """
        Return a Player object with attributes specified
        if no attributes specified, returns a game starting from the first inning
        """

        self.attr = {}
        self.attr["single"] = single
        self.attr["double"] = double
        self.attr["triple"] = triple
        self.attr["home_run"] = home_run
        self.attr["walk"] = walk
        self.attr["strikeout"] = strikeout
        self.attr["bbo"] = bbo

    def get_attr(self):
        return self.attr


class Game(object):
    """
    A 9-inning baseball game for the hitting team with the following properties:

    Attributes
        inning: integer tracking current inning (1-9)
        outs: integer tracking number of outs in current inning
        runners: dictionary of base, integer pairs corresponding to runners on base in current inning 
            i.e. {1:1, 2:0, 3:0} means runner on first
        score: integer tracking number of runs scored in game
        complete: boolean True if game complete, False otherwise
        lineup: list (representing a queue) of Player objects in lineup order
    """
    max_innings = 9
    max_outs = 3
    lineup_size = 9

    def __init__(self, inning=1, outs=0, runners={1: 0, 2: 0, 3: 0},
                 score=0, complete=False, lineup=([Player()]*lineup_size)):
        """
        Return a Game object with attributes specified
        If no attributes specified, returns a game starting from the first inning
        """
        self.inning = inning
        self.outs = outs
        self.runners = runners
        self.score = score
        self.complete = complete
        self.lineup = lineup

    def play_ball(self):
        """
        Plays the baseball game until completion i.e. until max_innings+1 is reached
        """
        while (self.inning <= self.max_innings):
            self.play_inning()
        self.complete = True

    def play_inning(self):
        """
        Plays (or finishes) current inning of game i.e. until max_outs is reached
        """
        while (self.outs < self.max_outs):
            current_hitter = self.lineup.pop(0)
            self.lineup.append(current_hitter)

            event = weighted_choice(current_hitter.get_attr())
            self.event_handler(event)

        self.inning += 1
        self.outs = 0
        self.runners = {1: 0, 2: 0, 3: 0}

    def event_handler(self, event):
        """
        Given event, calls appropriate event handler
        """
        if event == "single":
            self.single()
        elif event == "double":
            self.double()
        elif event == "triple":
            self.triple()
        elif event == "home_run":
            self.home_run()
        elif event == "walk":
            self.walk()
        elif event == "strikeout":
            self.strikeout()
        elif event == "bbo":
            self.bbo()
        else:
            assert False, "handle_event: unknown event given"

    def single(self):
        r = self.runners

        # Runner on third scores
        if r[3]:
            r[3] = 0
            self.score += 1

        # Runner on second makes it to third
        if r[2]:
            r[2] = 0
            r[3] = 1

        # Runner on first makes it to second
        if r[1]:
            r[1] = 0
            r[2] = 1

        # Hitter now on first
        r[1] = 1

    def double(self):
        r = self.runners

        # Runner on third scores
        if r[3]:
            r[3] = 0
            self.score += 1

        # Runner on second scores
        if r[2]:
            r[2] = 0
            self.score += 1

        # Runner on first makes it to third
        if r[1]:
            r[1] = 0
            r[3] = 1

        # Hitter now on second
        r[2] = 1

    def triple(self):
        r = self.runners

        # All runners score
        for key in r:
            if r[key]:
                r[key] = 0
                self.score += 1

        # Hitter now on third
        r[3] = 1

    def home_run(self):
        r = self.runners

        # All runners score
        for key in r:
            if r[key]:
                r[key] = 0
                self.score += 1

        # Hitter scores too and bases cleared
        self.score += 1

    def walk(self):
        # For now, treat as equivalent to single
        self.single()

    def strikeout(self):
        # Hitter out, increment outs
        self.outs += 1

    def bbo(self):
        # Hitter out, increment outs
        self.outs += 1


def main():
    g = Game()
    # print g.runners
    g.play_ball()
    print g.score

if __name__ == "__main__":
    main()
