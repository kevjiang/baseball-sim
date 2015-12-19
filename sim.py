from game import Game
from helpers import csv_to_lineup
from season import Season
from itertools import permutations
from copy import deepcopy
from random import shuffle
from math import ceil
import sys
import heapq



# simulate season for every permutation of lineup and rank lineups
# from most runs/game to least runs/game
def sim_and_rank_seasons(lineup, num_rotations=100):
    ordered_seasons = []  # stores seasons in descending order by runs/game
    counter = 0

    lineup_copy = lineup[:]

    while counter < num_rotations:
        # generate random rotation
        shuffle(lineup_copy)

        # test all 9 possible orders of given rotation
        for _ in range(9):
            lineup_copy.append(lineup_copy.pop(0))  # place first batter at end
            s = Season(lineup=deepcopy(list(lineup_copy)), num_games=162)
            s.play_season()
            ordered_seasons.append(s)

        counter += 1

    ordered_seasons.sort(key=lambda s: s.get_runs_per_game())

    # calculate average difference
    # best_run_total = 0
    # worst_run_total = 0
    # best_seasons = [ordered_seasons[-1], ordered_seasons[-2], ordered_seasons[-3], ordered_seasons[-4], ordered_seasons[-5]]
    # worst_seasons = [ordered_seasons[0], ordered_seasons[1], ordered_seasons[2], ordered_seasons[3], ordered_seasons[4]]
    # num_iter = 3

    # for seas in best_seasons:
    #     i = 0
    #     while i < num_iter:
    #         s = Season(lineup=deepcopy(list(seas.get_lineup())), num_games=162)
    #         s.play_season()
    #         best_run_total += s.get_runs_per_game()
    #         i += 1

    # for seas in worst_seasons:
    #     i = 0
    #     while i < num_iter:
    #         s = Season(lineup=deepcopy(list(seas.get_lineup())), num_games=162)
    #         s.play_season()
    #         worst_run_total += s.get_runs_per_game()
    #         i += 1

    # average_difference = (best_run_total - worst_run_total) / (num_iter*5)

    return ordered_seasons


# Returns:
# 1) sample top 5 best lineups
# 2) player, position, runs/game table
# 3) names_to_index table
# in a tuple

# Note: the position is indexed 0-8, but real positions are 1-9
# Note: cannot deal with lineups with duplicate names!  Must have unique named players!
def ordered_seasons_expl(ordered_seasons):
    if (len(ordered_seasons) < 5):
        print "Not enough ordered seasons: need more than 3"
        sys.exit()

    sample_best_seasons = [ordered_seasons[-1], ordered_seasons[-2], ordered_seasons[-3], ordered_seasons[-4], ordered_seasons[-5]]
    best_season = ordered_seasons[-1]
    best_lineup = best_season.get_lineup()
    lineup_size = len(best_lineup)
    name_to_index = {}  # dictionary converting names to an index

    for i, p in enumerate(best_lineup):
        if p in name_to_index:
            print "Error: cannot use duplicate names in lineup!"
            sys.exit()
        name_to_index[p.get_name()] = i

    #make list of lineups and associated runs per game (will be in descending run order)
    lineup_runs_list = []
    for s in ordered_seasons:
        lineup_runs_list.append([s.get_lineup(), s.get_runs_per_game()])

    #create matrix of players by batting position with [runs, games] in each entry
    temp_runs_matrix = [[[0, 0] for x in range(lineup_size)] for y in range(lineup_size)]

    for [lineup, runs] in lineup_runs_list:
        for position, player in enumerate(lineup):
            temp_runs_matrix[name_to_index[player.get_name()]][position][0] += runs
            temp_runs_matrix[name_to_index[player.get_name()]][position][1] += 1.0

    # contains runs/game in eacn entry instead of [runs, games]
    runs_matrix = [[[0, 0] for x in range(lineup_size)] for y in range(lineup_size)]
    for i, row in enumerate(temp_runs_matrix):
        for j, col in enumerate(row):
            if (col[1] < .001):  # i.e. dividing by 0
                runs_matrix[i][j] = 0.0
            else:
                runs_matrix[i][j] = col[0]/float(col[1])

    return (sample_best_seasons, runs_matrix, name_to_index)


#create file with explanation of best lineup
def explain_to_file(sample_best_seasons, runs_matrix, name_to_index, num_seasons):
    fp = open('final_report.txt', 'w')
    fp.write("Manager Report: Optimal Lineups\n\n")
    fp.write("TLDR: pick one of these lineups for the best value: \n")

    for i, season in enumerate(sample_best_seasons):
        fp.write("Lineup %d: \n" % (i+1))
        lineup = season.get_lineup()
        for j, player in enumerate(lineup):
            fp.write("%d): %s\n" % (j+1, player.get_name()))
        fp.write("Runs per game: %f \n" % (season.get_runs_per_game()))
        fp.write("\n")

    fp.write("blah blah blah; %d simulations\n\n" % (num_seasons))

    fp.write("\n%s\n" % ("Table of Runs Per Game Based on Players Batting Order Positions"))

    # create index_to_name dictionary from name_to_index dictionary
    index_to_name = dict((v, k) for k, v in name_to_index.iteritems())

    # title the columns
    fp.write("%25s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\n" % ("Player", "Pos 1", "Pos 2", "Pos 3", "Pos 4", "Pos 5", "Pos 6", "Pos 7", "Pos 8", "Pos 9"))

    # fill in the table
    for i, row in enumerate(runs_matrix):
        fp.write("%25s\t" % index_to_name[i])
        for j, col in enumerate(row):
            fp.write("%10f\t" % (runs_matrix[i][j]))
        fp.write("\n")
    fp.write("\n")

    # top 3 lineup spots per player
    # first, create dictionary with key as name and values as list with top 3 lineup spots
    top_lineup_spots_dic = {}
    for i in range(9):
        top_3_run_values = heapq.nlargest(3, runs_matrix[i])
        top_3_positions = []
        for v in top_3_run_values:
            for j, r in enumerate(runs_matrix[i]):
                if v == r:
                    top_3_positions.append(j+1)
                    break

        top_lineup_spots_dic[index_to_name[i]] = top_3_positions

    # next, write dictionary in easily readable format in file
    for i, row in enumerate(runs_matrix):
        top_3 = top_lineup_spots_dic[index_to_name[i]]
        fp.write("%25s:\t Best: %d, Better: %d, Good: %d\t" % (index_to_name[i], top_3[0], top_3[1], top_3[2]))
        fp.write("\n")

    print top_lineup_spots_dic

    fp.close()


#complete function call sequence to create and write to file for best lineup explanation
def best_lineup_complete(lineup, num_rotations=100):
    ordered_seasons = sim_and_rank_seasons(lineup, num_rotations)

    (sample_best_seasons, runs_matrix, name_to_index) = ordered_seasons_expl(ordered_seasons)

    explain_to_file(sample_best_seasons, runs_matrix, name_to_index, len(ordered_seasons))


# returns array indexed by lineup position of ordered seasons from worst to best
# the lineup position that generates the most RBIs for this player
# (and some sample ideal lineups)
def rbi_sim_and_rank_seasons(lineup, trials_per_pos=2, name="David Oritz"):
    lineup_copy = lineup[:]
    this_player = None
    this_player_index = -1
    ordered_seasons = [[] for _ in range(9)]  # list of list of seasons.  Index of list corresponds to player position

    # take player object of name out of lineup
    for i, p in enumerate(lineup_copy):
        if p.get_name() == name:
            if this_player is None:
                this_player = p
                this_player_index = i
                break
            else:  # menas duplicate player names!
                print "Error: cannot use duplicate names in lineup!"
                sys.exit()

    if this_player is None and this_player_index == -1:
        print "Player name not in lineup!"
        sys.exit()

    lineup_copy.pop(this_player_index)

    # test player at 1-9 spots of lineup
    for lineup_pos in range(9):
        for _ in range(trials_per_pos):
            shuffle(lineup_copy)  # randomize lineup
            lineup_copy.insert(lineup_pos, this_player)  # insert this player in appropriate spot

            s = Season(lineup=deepcopy(list(lineup_copy)), num_games=162)
            s.play_season()
            ordered_seasons[lineup_pos].append(s)

            for i, p in enumerate(lineup_copy):
                if p.get_name() == name:
                    del lineup_copy[i]
                    break

    return ordered_seasons

# return list with average RBIs generated at each position
def rbi_ordered_seasons_expl(lineup, ordered_seasons, name):
    lineup_copy = lineup[:]
    this_player = None

    # get player object from lineup
    for i, p in enumerate(lineup_copy):
        if p.get_name() == name:
            if this_player is None:
                this_player = p
                break


    average_rbis_position = []  # average rbi's player has by position

    for lis in ordered_seasons:
        rbis = 0
        count = 0.0
        for s in lis:
            this_player = None
            for p in s.get_lineup():
                if p.get_name() == name:
                    this_player = p
                    break
            rbis += this_player.get_stats_obj().get_stats_dic()["RBI"]
            count += 1.0
        average_rbis_position.append(rbis/count)

    return average_rbis_position

def rbi_explain_to_file(lineup, name, average_rbis_position, trials_per_pos):
    master = [(i + 1, elem) for i, elem in enumerate(average_rbis_position)]
    master.sort(key=lambda tup: tup[1])
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])

    fp = open('rbis_final_report.txt', 'w')
    fp.write("Player Report: Maximizing RBIs for %s\n\n" % (name))
    fp.write("TLDR: Ask (i.e. demand!) to bat in the %s spot in the lineup for maximal RBI production next season.\n\n" % (ordinal(master[-1][0])))

    fp.write("Best:      %d, Average RBIs: %.1f\n" % (master[-1][0], master[-1][1]))
    fp.write("Excellent: %d, Average RBIs: %.1f\n" % (master[-2][0], master[-2][1]))
    fp.write("Great:     %d, Average RBIs: %.1f\n" % (master[-3][0], master[-3][1]))
    fp.write("Good:      %d, Average RBIs: %.1f\n" % (master[-4][0], master[-4][1]))
    fp.write("Passable:  %d, Average RBIs: %.1f\n" % (master[-5][0], master[-5][1]))
    fp.write("Poor:      %d, Average RBIs: %.1f\n" % (master[-6][0], master[-6][1]))
    fp.write("Bad:       %d, Average RBIs: %.1f\n" % (master[-7][0], master[-7][1]))
    fp.write("Horrible:  %d, Average RBIs: %.1f\n" % (master[-8][0], master[-8][1]))
    fp.write("Worst:     %d, Average RBIs: %.1f\n\n" % (master[-9][0], master[-9][1]))

    fp.write("blah blah blah, explain lineup simulations and salary to RBIs correlation; %d simulations\n\n" % (trials_per_pos*9))

    fp.close()
    return


def maximize_rbi_complete(lineup, trials_per_pos=2, name="David Oritz"):
    ordered_seasons = rbi_sim_and_rank_seasons(lineup, trials_per_pos, name)
    average_rbis_position = rbi_ordered_seasons_expl(lineup, ordered_seasons, name)
    rbi_explain_to_file(lineup, name, average_rbis_position, trials_per_pos)
    return


def main():
    # lineup = csv_to_lineup('bos_2004_ws_g2.csv')
    lineup = csv_to_lineup('bos_2015_random_order.csv')
    print "***And the lineup is...***"
    for elem in lineup:
        print "1: " + str(elem) + ", " + str(elem.get_attr_obj().get_attr_dic())
    print "**************************"

    # num_sim = 162
    # total_score = 0

    # for _ in range(num_sim):
    #     g = Game(live_update=True, game_summary=True, lineup=lineup)
    #     g.play_ball()
    #     total_score += g.get_score()

    # print total_score/float(num_sim)

    # s = Season(lineup=lineup)
    # s.play_season()
    # s.print_season_summary()
    # print "Runs per game: " + str(s.get_runs_per_game())

    # best_lineup_complete(lineup, num_rotations=2)
    maximize_rbi_complete(lineup, trials_per_pos=2, name="David Ortiz")


if __name__ == "__main__":
    main()
