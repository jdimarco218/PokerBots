#!/usr/bin/python
import sys
sys.path.insert(0, 'src')
stdout = sys.stdout
sys.stdout = open('results/results.txt', 'w')

from PokerPlayerJeff import *
from PokerPlayerOpp import *
from HeadsUp import *

# Create players and controlle
pgc = PokerGameController( 1, 10000)
ppOpponent = PokerPlayerOpp("Opponent", pgc)
ppJeff = PokerPlayerJeff("Jeff", pgc)
input_player_list = [ppOpponent, ppJeff]

pgc.initGame(input_player_list)
pgc.runGame()
