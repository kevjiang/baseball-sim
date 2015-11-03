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

    Properties
        inning: integer tracking current inning (1-9)
        outs: integer tracking number of outs in current inning
        runners: dictionary of base, Player() pairs corresponding to runners on base in current inning
            i.e. {1:Player(), 2:None, 3:0} means runner on first
        score: integer tracking number of runs scored in game
        hits: integer tracking number of hits
        complete: boolean True if game complete, False otherwise
        lineup: list (representing a queue) of Player objects in lineup order
        live_update: True if want printed updates of game, False otherwise
    """
    max_innings = 9
    max_outs = 3
    lineup_size = 9

    def __init__(self, inning=1, outs=0, runners={1: None, 2: None, 3: None},
                 score=0, total_hits=0, complete=False,
                 lineup=([Player()]*lineup_size), live_update=False):
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
        self.live_update = live_update

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

            event = weighted_choice(current_hitter.get_attr_obj().get_attr_dic())
            self.event_handler(event, current_hitter)

            if self.live_update:
                self.play_by_play(event, current_hitter)

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

        # Runner on third scores (99% certain Levitt 1999)
        if r[3]:
            r[3] = None
            self.score += 1

        # Runner on second
        if r[2]:
            prob_dic = {"2-2": 12, "2-3": 299, "2-h": 653, "2-x": 36}
            event = weighted_choice(prob_dic)
            if event == "2-2":
                r[2] = r[2]
            elif event == "2-3":
                r[3] = r[2]
                r[2] = None
            elif event == "2-h":
                r[2] = None
                self.score += 1
            elif event == "2-x":
                r[2] = None
                self.outs += 1
            else:
                assert False, "single: Shouldn't get here"

        # Runner on first
        if r[1]:
            prob_dic = {"1-2": 652, "1-3": 313, "1-h": 14, "1-x": 21}
            event = weighted_choice(prob_dic)
            if event == "1-2":
                r[2] = r[1]
                r[1] = None
            elif event == "1-3":
                r[3] = r[1]
                r[1] = None
            elif event == "1-h":
                r[1] = None
                self.score += 1
            elif event == "1-x":
                r[1] = None
                self.outs += 1
            else:
                assert False, "single: Shouldn't get here"

        # Hitter now on first
        r[1] = player
        self.total_hits += 1

    def double(self, player):
        r = self.runners

        # Runner on third scores
        if r[3]:
            r[3] = None
            self.score += 1

        # Runner on second scores (98.4% certain Levitt 1999)
        if r[2]:
            r[2] = None
            self.score += 1

        # Runner on first has three possible outcomes based on Levitt (1999)
        # 1) 1-3 536
        # 2) 1-h 433
        # 4) 1-x 31
        if r[1]:
            prob_dic = {"1-3": 536, "1-h": 433, "1-x": 31}
            event = weighted_choice(prob_dic)
            if event == "1-3":
                r[3] = r[1]
                r[1] = None
            elif event == "1-h":
                r[1] = None
                self.score += 1
            elif event == "1-x":
                r[1] = None
                self.outs += 1
            else:
                assert False, "double: Shouldn't get here"

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

        r = self.runners

        # If runner on 1,2,3, runner on third scores
        if r[1] and r[2] and r[3]:
            r[3] = None
            self.score += 1

        # If runner on 1,2, runner on second moves to third
        if r[1] and r[2]:
            r[3] = r[2]
            r[2] = None

        # If runner on 1, moves to second
        if r[1]:
            r[2] = r[1]
            r[1] = None

        # Hitter now on first
        r[1] = player

    def strikeout(self, player):
        # Hitter out, increment outs
        self.outs += 1

    def bbo(self, player):
        # Hitter out, increment outs
        self.outs += 1

    def play_by_play(self, event, player):
        print "Inn: " + str(self.inning) + " Outs: " + str(self.outs) + \
            " Score: " + str(self.score) + " " + \
            str(player) + ", " + event + " 1: " + str(self.runners[1]) + \
            ", 2: " + str(self.runners[2]) + \
            ", 3: " + str(self.runners[3])
