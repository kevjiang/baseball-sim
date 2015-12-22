<h5>See kjiang_project_proposal.doc for a detailed overview of the design structure, implementation, and motivation behind this baseball sim.</h5>

example_final_manager_report_bos_2004_ws.txt contains a sample manager simulation output for the Boston Red Sox 2004 World Series lineup.  This output contains detailed information directed at the manager of the team for maximizing runs scored per game through lineup optimization.  Player data was obtained from bos_2004_ws_g2.csv.

example_final_player_report_bos_2004_ws.txt contains a sample player simulation output for David Ortiz in the context of the eight other players in the Boston Red Sox 2004 World Series lineup.  This output contains detailed information directed at David Ortiz (a player on the Red Sox) for maximizing his RBIs produced through lineup optimization.  Player data was obtained from bos_2004_ws_g2.csv.

The above two outputs represent a rather large simulation sample size.  Each simulation processed 16,200 seasons, which is equivalent to 2,624,400 games, 23,619,600 innings, or about 99,202,320 player plate appearances.  Processing these simulations, recording individual player statistics etc. requires quite a bit of processing power, and as such, it is probably infeasible for you to run the program with this many seasons.  Thus, I have provided 2 calling sequences, (A) to generate a manager report in final_manager_report.txt and (B) to generate a player report in final_player_report.txt that simulates 180 seasons each-- as such, it should take a significantly shorter amount of time.  (-) represents the general calling sequence.  Note that the number of seasons actually simulated will be [num_rotations|trials_per_pos] * 9.  

Command line calling sequence:
(-) python sim.py [player_name] input_file num_rotations|trials_per_pos output_file
(A) python sim.py bos_2004_ws_g2.csv 20 final_manager_report.txt
(B) python sim.py 'David Ortiz' bos_2004_ws_g2.csv 20 final_player_report.txt

When running these commands on the zoo, I had it take about 30 seconds to run.

See github repo to learn more: https://github.com/kevjiang/baseball-sim
