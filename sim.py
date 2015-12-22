from helpers import csv_to_lineup
from season import Season
from copy import deepcopy
from random import shuffle
import sys
import heapq


# simulate season for every permutation of lineup and rank lineups
# from most runs/game to least runs/game
def sim_and_rank_seasons(lineup, num_rotations=2):
    ordered_seasons = []  # stores seasons in descending order by runs/game
    counter = 0

    lineup_copy = lineup[:]

    while counter < num_rotations:
        # generate random rotation
        shuffle(lineup_copy)

        # test all 9 possible orders of given rotation
        for i in range(9):
            lineup_copy.append(lineup_copy.pop(0))  # place first batter at end
            s = Season(lineup=deepcopy(list(lineup_copy)), num_games=162)
            s.play_season()
            ordered_seasons.append(s)

            #print to terminal so people don't freak out waiting for simulations to end
            sys.stdout.write("\rSeasons Simulated: %d/%d" % (i+counter*9+1, num_rotations*9))
            sys.stdout.flush()

        counter += 1

    ordered_seasons.sort(key=lambda s: s.get_runs_per_game())

    sys.stdout.write("\n")

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
def explain_to_file(sample_best_seasons, runs_matrix, name_to_index, num_seasons, output_file):
    fp = open(output_file, 'w')
    fp.write("Manager Report: Optimal Lineups\n\n")
    fp.write("To the Manager:\n\n")
    fp.write("\tAs you know, in the sport of baseball, you must make a decision on how to order the nine hitters in a lineup.  Much has been written and researched about this topic throughout the past century.  You likely have heard a lot of \"conventional lineup wisdom\" which suggests various rules of thumb, such as placing the fastest hitter as the leadoff man (1st), the best power hitter as the cleanup hitter (4th), or the highest average hitter in the 3rd spot.\n\n")
    fp.write('\tThe bad news is that the "conventional lineup wisdom" of old is based largely on "gut feelings", which do not necessarily result in winning lineup combinations.  While conventional wisdom may be smart to follow loosely, it is perhaps easy to see that monolithic advice such as "place the highest average hitter in the 3rd spot" without considering other variables such as the composition of the rest of the lineup is a sub-optimal lineup-building approach.  The good news is that you, as the manager, need not follow outdated, data-blind rules when setting your lineup-- instead, by following the lineup suggestions in this report, you can construct a lineup to be as close to optimal as possible.\n\n')
    fp.write('\tI am well aware that the batting order is not constructed in a vacuum-- that is, you as a manager have player egos to manage and as such will be "forced" through external, social factors to bat certain players at certain positions.  This is why this report offers, in addition to the five most optimal lineup combinations, a detailed analysis of which positions a player should bat to optimize lineup performance.  Thus, you as a manager will be able to make an informed decision balancing the various pressures of managing a clubhouse with constructing a lineup that offers the maximum number of runs per game.\n\n')
    fp.write('\tOur data driven approach will simulate full 162-game seasons of baseball using a baseball simulation engine.  Seasons will be simulated using different permutations of a 9-person batting lineup, and the runs/game from each season will be recorded, processed, and evaluated to find 1) optimal batting positions for each player and 2) the top 5 optimal lineups.  Player historical statistics will be used as an input as an estimate of future performance-- that is, our report generates optimal lineup data assuming that players will play to their previously statistical ability.  However, if you suspect a player\'s abilities have significantly deviated from their historical performance, it would be easy to add these new observations by altering the statistical data contained in the input csv files to our simulation engine (or ask your resident computer/data science professional to change these values for you).\n\n')
    fp.write('\tIf you are short on time, below are 5 of the optimal lineups based on maximizing runs/game that appeared in our simulations.  In addition to runs/game data, we have also included the statistical output of each player during that season, which should give you a sense of how each player fared in our simulated season.  This data is included because the variance in baseball, even in a 162-game season, can be admittedly high-- thus, if you notice that a player over-performed or under-performed in the season in question, you can adjust your lineup evaluations accordingly.  Regardless, using one of these lineup combinations in real MLB games should allow for a relatively optimal performance.\n\n')
    fp.write("\tNote: This report was generated using %d Monte Carlo simulations of 162-game seasons.\n\n" % (num_seasons))
    fp.write('\tTLDR: pick one of these lineups for your optimal lineup combination:\n\n')

    for i, season in enumerate(sample_best_seasons):
        fp.write("Lineup %-21d\t%-6s\t%-6s\t%-6s\t%-6s\t%-6s\t%-6s\t%-6s\t%-6s\t%-6s\t%-6s\n" % (i+1, "AVG", "HR", "RBI", "OBP", "SLG", "AB", "H", "R", "BB", "SO"))
        lineup = season.get_lineup()
        for j, player in enumerate(lineup):
            stats = player.get_stats_obj().get_stats_dic()
            fp.write("%d) %-25s\t%-6.3f\t%-6d\t%-6d\t%-6.3f\t%-6.3f\t%-6d\t%-6d\t%-6d\t%-6d\t%-6d\n" % (j+1, player.get_name(), stats["AVG"], stats["HR"], stats["RBI"], stats["OBP"], stats["SLG"], stats["AB"], stats["H"], stats["R"], stats["BB"], stats["SO"]))

        fp.write("Runs per game: %.3f \n" % (season.get_runs_per_game()))
        fp.write("\n")

    fp.write('\n\tIf you are willing to dig deeper into the data, this report also provides a more holistic evaluation of player viability at different positions. Below is a table that displays the average runs per game of a lineup containing a given player at a given batting position (i.e. the average number of runs per game generated when player X batted in the ith spot in the lineup).  \n\n')
    fp.write('\tUsing this table provided, you will be able to judge how many runs per game an average lineup with a particular player at a particular position will produce.  Each player has batting positions that result in lineups that produce more runs; likewise, every player has batting positions that result in lineups that produce fewer runs.  The key for you as a manager is to place as many players in their \"optimal\" batting positions as possible, in order to produce an optimally performing lineup.  However, it is also important to note that this data is based on an \"average\" lineup-- thus, you should also refer to the 5 optimal lineups for a good idea of optimal orderings in which to place your players, and balance the two pieces of information in addition to other external, social pressures accordingly.\n\n')
    fp.write("%s\n" % ("Table of Runs Per Game Based on Player Batting Order Positions"))

    # create index_to_name dictionary from name_to_index dictionary
    index_to_name = dict((v, k) for k, v in name_to_index.iteritems())

    # title the columns
    fp.write("%-28s\t%-6s\t%-6s\t%-6s\t%-6s\t%-6s\t%-6s\t%-6s\t%-6s\t%-6s\n" % ("Player", "Pos 1", "Pos 2", "Pos 3", "Pos 4", "Pos 5", "Pos 6", "Pos 7", "Pos 8", "Pos 9"))

    # fill in the table
    for i, row in enumerate(runs_matrix):
        fp.write("%-28s\t" % index_to_name[i])
        for j, col in enumerate(row):
            fp.write("%-6.3f\t" % (runs_matrix[i][j]))
        fp.write("\n")
    fp.write("\n")

    fp.write("\tFinally, in lieu of the \"conventional lineup wisdom\" of old, this report has generated a data driven lineup cheat sheet, which will provide the top 3 lineup positions for each player based on these Monte Carlo simulations.  Note that it may not be possible to place all players in their \"best\" position (since one player's optimal position in a lineup could feasibly be the same as another player's optimal position in a lineup).  However, you should try your best to place a player in one of their three most optimal batting positions.\n\n")

    # top 3 lineup spots per player
    # first, create dictionary with key as name and values as list with top 3 lineup spots
    fp.write("Lineup Wisdom Cheat Sheet\n")
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
        fp.write("%-28s\tBest: %d\tBetter: %d\tGood: %d\n" % (index_to_name[i], top_3[0], top_3[1], top_3[2]))

    fp.write("\n\tA caveat: it is important to note that, due to the high variance of the sport of baseball and the nature of Monte Carlo simulations, subsequent reports generated by our baseball engine may produce slightly different results.  It is important to run an adequately high number of simulations (we suggest >1000 total different seasons as a starting point, but really the more simulations run the more accurate the data will be) for a more complete report.  If you suspect that some of the optimal lineups were flukes, that's ok!  In fact, that's why this report includes five optimal lineups in addition to the statistics of each player in those lineups-- due diligence on your part as a manager should be able to weed out any aggregiously anamolous player performances using the data provided in this report. \n")
    fp.write("\n\tSincerely,\n\n\tKevin Jiang, Automated Decision System \"Expert\"\n")
    fp.close()


#complete function call sequence to create and write to file for best lineup explanation
def best_lineup_complete(lineup, num_rotations=2, output_file="final_manager_report.txt"):
    ordered_seasons = sim_and_rank_seasons(lineup, num_rotations)
    (sample_best_seasons, runs_matrix, name_to_index) = ordered_seasons_expl(ordered_seasons)
    explain_to_file(sample_best_seasons, runs_matrix, name_to_index, len(ordered_seasons), output_file)
    sys.stdout.write("%s %s\n" % ("Simulations complete.  Find full manager report in file:", output_file))
    return


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
    counter = 0
    for lineup_pos in range(9):
        for i in range(trials_per_pos):
            shuffle(lineup_copy)  # randomize lineup
            lineup_copy.insert(lineup_pos, this_player)  # insert this player in appropriate spot

            s = Season(lineup=deepcopy(list(lineup_copy)), num_games=162)
            s.play_season()
            ordered_seasons[lineup_pos].append(s)

            for i, p in enumerate(lineup_copy):
                if p.get_name() == name:
                    del lineup_copy[i]
                    break

            #print to terminal so people don't freak out waiting for simulations to end
            sys.stdout.write("\rSeasons Simulated: %d/%d" % (counter+1, trials_per_pos*9))
            sys.stdout.flush()
            counter += 1

    sys.stdout.write("\n")

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


def rbi_explain_to_file(lineup, name, average_rbis_position, trials_per_pos, output_file):
    master = [(i + 1, elem) for i, elem in enumerate(average_rbis_position)]
    master.sort(key=lambda tup: tup[1])
    ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(n/10 % 10 != 1) * (n % 10 < 4) * n % 10::4])

    # fp = open('final_player_report.txt', 'w')
    fp = open(output_file, 'w')
    fp.write("%s %s\n\n" % ("Player Report: Maximizing RBIs for", name))

    fp.write("\t%s\n\n" % ("As you know, where you bat in the order matters.  \"Conventional wisdom\" suggests that hitting near the top of the lineup signals that you are an integral part of the lineup and that your manager respects your hitting abilities; hitting near the bottom of the lineup is a sign that you may soon be riding the bench.  Perhaps you have it in your head that you are a powerful cleanup hitter and thus must always bat fourth.  Perhaps your identity as a top-of-the-order speedster makes you demand to bat first in the order.  "))
    fp.write("\t%s\n\n" % ('However, if your goal is to win the Triple Crown, that is finish with the (1) highest batting average, (2) number of home runs, and (3) number of RBIs in the league, then you should pick a batting lineup position that maximizes your RBI count (average and home runs is decided by your skill level alone unfortunately, so no amount of batting position tweaks can help you in that cause).  This elusive title is only reached about once every two decades-- why not maximize your chances?'))
    fp.write("\t%s\n\n" % ('Perhaps your ambitions are not to win the Triple Crown.  But, if you are looking to make the most money in your baseball career, your preferences for batting order position should be simple; simply put, you should want to bat in the position that nets you the highest number of RBIs as well!  RBIs (if someone other than a baseball aficionado is reading this report) is the number of runs batted in for a given hitter; that is, the number of runs that scored directly as a result of your at bats.  The only way to guarantee an RBI is to hit a homerun and thus score yourself-- otherwise, RBIs depend entirely on the actions of the players who hit before you.  In other words, RBIs are almost entirely dependent on your position in the lineup!  Research has shown time and time again that RBI production correlates strongly with salary earnings-- a study done by the University of Arizona showed that salary and RBI production correlated with an r value of +.737.  Although admittedly correlation does not imply causation, since we can severely alter the number of RBIs a player produces in a season by simply changing your spot in the batting order, it does not hurt to try and maximize this statistic--at best, a (perhaps fool-hardy) general manager will pay you a few million dollars more per year due to your inflated RBI total.'))
    fp.write("\t%s\n\n" % ("Thus, this report's goal will be to pick the batting position in the lineup (1-9) that yields on average the most RBIs in our simulations given your talent level based on previous historical batting data."))
    fp.write("\t%s\n\n" % ('To calculate the best batting position for you given the eight players that will be batting with you, this report will use a Monte Carlo simulation to run through full 162-game seasons of baseball using a baseball simulation engine. Since managers often will swap around player batting orders during a season, we will generate random assortments of lineups for each batting position we place you in-- then we will calculate the average number of RBIs you produce each season you bat in that position of the lineup.  '))
    fp.write("\t%s%d%s\n\n" % ('The following includes the results from ',  trials_per_pos*9, ' Monte Carlo simulations.'))

    fp.write("\tBest:      %d, Average RBIs: %.1f\n" % (master[-1][0], master[-1][1]))
    fp.write("\tExcellent: %d, Average RBIs: %.1f\n" % (master[-2][0], master[-2][1]))
    fp.write("\tGreat:     %d, Average RBIs: %.1f\n" % (master[-3][0], master[-3][1]))
    fp.write("\tGood:      %d, Average RBIs: %.1f\n" % (master[-4][0], master[-4][1]))
    fp.write("\tPassable:  %d, Average RBIs: %.1f\n" % (master[-5][0], master[-5][1]))
    fp.write("\tPoor:      %d, Average RBIs: %.1f\n" % (master[-6][0], master[-6][1]))
    fp.write("\tBad:       %d, Average RBIs: %.1f\n" % (master[-7][0], master[-7][1]))
    fp.write("\tHorrible:  %d, Average RBIs: %.1f\n" % (master[-8][0], master[-8][1]))
    fp.write("\tWorst:     %d, Average RBIs: %.1f\n\n" % (master[-9][0], master[-9][1]))

    fp.write("\tThus, ask (i.e. demand!) your manager to bat in the %s spot in the lineup for maximal RBI production next season.  Whether your goals are to maximize your chance for the Triple Crown or simply maximize the money you earn on your next contract, this is an easy way to ensure that you are not being cheated by your lineup position!\n\n" % (ordinal(master[-1][0])))
    fp.write("\t%s\n\n" % ("A final caveat: it is important to note that, due to the high variance of the sport of baseball and the nature of Monte Carlo simulations, subsequent reports generated by our baseball engine may produce slightly different results.  It is important to run an adequately high number of simulations (we suggest >1000 total different seasons) for a more complete report."))

    fp.write("\n\tSincerely,\n\n\tKevin Jiang, Automated Decision Systems \"Expert\"\n")
    fp.close()
    return


def maximize_rbi_complete(lineup, trials_per_pos=2, name="David Oritz", output_file="final_player_report.txt"):
    ordered_seasons = rbi_sim_and_rank_seasons(lineup, trials_per_pos, name)
    average_rbis_position = rbi_ordered_seasons_expl(lineup, ordered_seasons, name)
    rbi_explain_to_file(lineup, name, average_rbis_position, trials_per_pos, output_file)
    sys.stdout.write("%s %s\n" % ("Simulations complete.  Find full player report in file:", output_file))
    return


def main():
    # python sim.py [player_name if player] input_file num_rotations/trials_per_pos output_file
    # python sim.py bos_2004_ws_g2.csv 20 final_manager_report.txt
    # python sim.py 'David Ortiz' bos_2004_ws_g2.csv 20 final_player_report.txt
    if len(sys.argv) == 4:  # means file a manager report
        input_file = sys.argv[1]
        num_rotations = int(sys.argv[2])
        output_file = sys.argv[3]

        lineup = csv_to_lineup(input_file)

        best_lineup_complete(lineup, num_rotations=num_rotations, output_file=output_file)

    elif len(sys.argv) == 5:
        player_name = sys.argv[1]
        input_file = sys.argv[2]
        trials_per_pos = int(sys.argv[3])
        output_file = sys.argv[4]

        lineup = csv_to_lineup(input_file)

        maximize_rbi_complete(lineup, trials_per_pos=trials_per_pos, name=player_name, output_file=output_file)

    else:
        print "Command Line Argument Error, See ReadMe for Correct Calling Sequences"
        print len(sys.argv)
        exit(0)

    return


if __name__ == "__main__":
    main()
