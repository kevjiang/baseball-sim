'''
Time For 1 million game runs
7.216486

real    3m29.357s
'''

import random
from player import Player

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


class Game(object):
    """
    A 9-inning baseball game for the hitting team with the following properties:

    Attributes
        inning: integer tracking current inning (1-9)
        outs: integer tracking number of outs in current inning
        runners: dictionary of base, Player() pairs corresponding to runners on base in current inning
            i.e. {1:Player(), 2:None, 3:0} means runner on first
        score: integer tracking number of runs scored in game
        hits: integer tracking number of hits
        complete: boolean True if game complete, False otherwise
        lineup: list (representing a queue) of Player objects in lineup order
    """
    max_innings = 9
    max_outs = 3
    lineup_size = 9

    def __init__(self, inning=1, outs=0, runners={1: None, 2: None, 3: None},
                 score=0, total_hits=0, complete=False,
                 lineup=([Player()]*lineup_size)):
        """
        Return a Game object with attributes specified
        If no attributes specified, returns a game starting from the first inning
        """
        self.inning = inning
        self.outs = outs
        self.runners = runners
        self.score = score
        self.total_hits = total_hits
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
            print self.runners
            self.event_handler(event, current_hitter)

        self.inning += 1
        self.outs = 0
        self.runners = {1: None, 2: None, 3: None}

    def event_handler(self, event, player):
        """
        Given event, calls appropriate event handler
        """
        if event == "single":
            self.single(player)
        elif event == "double":
            self.double(player)
        elif event == "triple":
            self.triple(player)
        elif event == "home_run":
            self.home_run(player)
        elif event == "walk":
            self.walk(player)
        elif event == "strikeout":
            self.strikeout(player)
        elif event == "bbo":
            self.bbo(player)
        else:
            assert False, "handle_event: unknown event given"

    def single(self, player):
        r = self.runners

        # Runner on third scores
        if r[3]:
            r[3] = None
            self.score += 1

        # Runner on second makes it to third
        if r[2]:
            temp = r[2]
            r[2] = None
            r[3] = temp

        # Runner on first makes it to second
        if r[1]:
            temp = r[1]
            r[1] = None
            r[2] = temp

        # Hitter now on first
        r[1] = player
        self.total_hits += 1

    def double(self, player):
        r = self.runners

        # Runner on third scores
        if r[3]:
            r[3] = None
            self.score += 1

        # Runner on second scores
        if r[2]:
            r[2] = None
            self.score += 1

        # Runner on first makes it to third
        if r[1]:
            temp = r[1]
            r[1] = None
            r[3] = temp

        # Hitter now on second
        r[2] = player
        self.total_hits += 1

    def triple(self, player):
        r = self.runners

        # All runners score
        for key in r:
            if r[key]:
                r[key] = None
                self.score += 1

        # Hitter now on third
        r[3] = player
        self.total_hits += 1

    def home_run(self, player):
        r = self.runners

        # All runners score
        for key in r:
            if r[key]:
                r[key] = None
                self.score += 1

        # Hitter scores too and bases cleared
        self.score += 1
        self.total_hits += 1

    def walk(self, player):
        # For now, treat as equivalent to single
        self.single(player)

    def strikeout(self, player):
        # Hitter out, increment outs
        self.outs += 1

    def bbo(self, player):
        # Hitter out, increment outs
        self.outs += 1


def main():
    num_sim = 100000
    total_score = 0
    # print g.runners
    for _ in range(num_sim):
        g = Game()
        g.play_ball()
        total_score += g.score

    print total_score/float(num_sim)

if __name__ == "__main__":
    main()
