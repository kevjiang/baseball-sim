from game import Game
from helpers import csv_to_lineup


def main():
    lineup = csv_to_lineup('bos_2004_ws_g2.csv')
    for elem in lineup:
        print str(elem) + ", " + str(elem.get_attr_obj().get_attr_dic())

    num_sim = 162
    total_score = 0

    for _ in range(num_sim):
        g = Game(live_update=True, game_summary=True, lineup=lineup)
        g.play_ball()
        total_score += g.get_score()

    print total_score/float(num_sim)

if __name__ == "__main__":
    main()
