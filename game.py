

class Game(object):
    """
    A 9-inning baseball game for the hitting team with the following properties:

    Attributes
        inning: integer tracking current inning (1-9)
        outs: integer tracking number of outs in current inning
        runners: list of (0,1) integers corresponding to runners on base in current inning [first, second, third]
        score: integer tracking number of runs scored in game
        complete: boolean True if game complete, False otherwise
    """
    max_innings = 9
    max_outs = 3

    def __init__(self, inning=1, outs=0, runners=[0,0,0], score=0, complete=False):
        """
        Return a Game object with attributes specified
        if no attributes specified, returns a game starting from the first inning
        """
        self.inning = inning
        self.outs = outs
        self.runners = runners
        self.score = score
        self.complete = complete

    def play_ball(self):
        """
        plays the baseball game until completion i.e. until max_innings+1 is reached
        """
        while (self.inning <= max_innings):
            play_inning()
        self.complete = True

    def play_inning(self):
        """
        plays (or finishes) current inning of game i.e. until max_outs is reached
        """
        while (self.outs < max_outs):
            #here's where you would pop the player from queue

        self.inning += 1
        self.outs = 0
        self.runners = [0,0,0]

    def set_balance(self, balance=0.0):
        """Set the customer's starting balance."""
        self.balance = balance

    def withdraw(self, amount):
        """Return the balance remaining after withdrawing *amount*
        dollars."""
        if amount > self.balance:
            raise RuntimeError('Amount greater than available balance.')
        self.balance -= amount
        return self.balance

    def deposit(self, amount):
        """Return the balance remaining after depositing *amount*
        dollars."""
        self.balance += amount
        return self.balance

class Player(object):
    """
    A player with the following attributes:

    Attributes
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
        
        self.single = single
        self.double = double
        self.triple = triple
        self.home_run = home_run
        self.walk = walk
        self.strikeout = strikeout
        self.bbo = bbo




