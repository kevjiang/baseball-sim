


Calling sequence:
python sim.py [player_name] input_file [num_rotations|trials_per_pos] output_file
Ex 1) python sim.py bos_2004_ws_g2.csv 20 final_manager_report.txt
Ex 2) python sim.py 'David Ortiz' bos_2004_ws_g2.csv 20 final_player_report.txt

# baseball-sim
RBI vs. salary: https://ai.arizona.edu/sites/ai/files/MIS580/baseball.pdf

baseball sim ideas (esp. baserunning probabilities): http://knology.net/johnfjarvis/simulator.html

another baserunning table: https://books.google.com/books?id=E_NCXcE6J2EC&pg=PA104&lpg=PA104&dq=baseball+simulator+runner+advancement+player+speed&source=bl&ots=EnLF5Qa-Sx&sig=6ua4q9jLGwwODIfOyPtNyS8Pblw&hl=en&sa=X&ved=0CB0Q6AEwAGoVChMIk9Lq9fb0yAIVQn-QCh3yqQiX#v=onepage&q=baseball%20simulator%20runner%20advancement%20player%20speed&f=false

Markov Model Explanation: http://www.pankin.com/markov/btn1191.htm

To do
3) Baserunning based on real player data
4) Steal potential.
5) Error potential.  
6) Sacrifce potential.  
7) Baserunner movement on bbo potential
8) Add pitchers to the mix
9) Figure out why runs are about 1 run/game too high!  (or maybe it's valid?)

maybe not to do
a) maybe add lineup class? but probably not
b) Maybe make a new Innings class to represent an inning

Time:
1000 162 game season simulations: 3min 40 s = 220s