#!/usr/bin/python

import os
import sys
sys.path.insert(0, 'src')

from PokerPlayerJeff import *
from PokerPlayerOpp import *
from HeadsUp import *

# Setup file and direct prints to results/results.txt
if os.path.isfile('./results/results.txt'):
    os.remove('./results/results.txt')
stdout = sys.stdout
sys.stdout = open('./results/results.txt', 'w')


# Create players and controlle
pgc = PokerGameController( 1, 10000)
ppOpponent = PokerPlayerOpp("Opponent", pgc)
ppJeff = PokerPlayerJeff("Jeff", pgc)
input_player_list = [ppOpponent, ppJeff]

pgc.initGame(input_player_list)
pgc.runGame()

# Reset stdout
sys.stdout = stdout
if pgc.game_state.player_chips["Jeff"] > pgc.game_state.player_chips["Opponent"]:
    print "Jeff wins!"
else:
    print "Opponent wins!"

