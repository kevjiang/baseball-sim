import random
import csv
from player import Player, Stats, Attr


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
                                strikeout=a['SO'], bbo=a['AB']-a['H']-a['SO']),
                      stats=Stats()))
    return lineup
