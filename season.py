from player import Player
from game import Game


class Season(object):
    """
    A season that can simulate 162 (or custom value) games for a given lineup

    Properties
        lineup: list of players in lineup order
        num_games:  number of games by default
        season_summary: True if want printed season summary, False otherwise
    """
    lineup_size = 9

    def __init__(self, lineup=([Player()]*lineup_size), num_games=162,
                 season_summary=False):
        self.num_games = num_games
        self.lineup = lineup[:]
        self.season_summary = season_summary
        self.total_score = 0

    def play_season(self):
        for _ in range(self.num_games):
            g = Game(lineup=self.lineup)
            g.play_ball()
            self.total_score += g.get_score()

    def season_summary(self):
        for player in self.lineup:
            print player.get_name() + ": " + str(player.get_stats_obj().get_stats_dic())
