from game import Game
from player import Player, Stats, Attr
import csv


# converts fangraphs csv file to a list of all players in file and returns lineup
def csv_to_lineup(filename):
    csvfile = open(filename, 'rU')
    reader = csv.reader(csvfile)
    column_names = next(reader)
    attr_dic_list = []

    for attr_list in reader:  # append player stats to list
        attr_dic = {}
        for i in range(len(attr_list)):
            value = attr_list[i]
            key = column_names[i]
            if key != 'Name':  # two special cases: Name and AVG
                if key != 'AVG':
                    value = int(attr_list[i])
                else:
                    value = float(attr_list[i])
            attr_dic[key] = value
        attr_dic_list.append(attr_dic)

    lineup = []
    for a in attr_dic_list:  # add player objects to lineup
        lineup.append(Player(
                      name=a['Name'],
                      attr=Attr(single=a['1B'], double=a['2B'], triple=a['3B'],
                                home_run=a['HR'], walk=a['BB']+a['IBB']+a['HBP'],
                                strikeout=a['SO'], bbo=a['AB']-a['H']),
                      stats=Stats()))
    return lineup


def main():
    lineup = csv_to_lineup('bos_2004_ws_g2.csv')
    for elem in lineup:
        print str(elem)

    # return
    # print players
    # return
    num_sim = 1000
    total_score = 0

    for _ in range(num_sim):
        g = Game(live_update=False, lineup=lineup)
        g.play_ball()
        total_score += g.score

    print total_score/float(num_sim)

if __name__ == "__main__":
    main()
