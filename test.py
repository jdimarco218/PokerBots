#!/usr/bin/python

from PokerPlayerJeff import *
from PokerPlayerOpp import *
from PokerPlayerAllInBot import *
from PokerGame import *

pgc = PokerGameController( 1, 600)
ppo1 = PokerPlayerOpp("Opponent 1", pgc)
ppo2 = PokerPlayerOpp("Opponent 2", pgc)
#ppo3 = PokerPlayerAllInBot("All In Bot", pgc)
ppo4 = PokerPlayerOpp("Opponent 4", pgc)


input_player_list = []
input_player_list.append(ppo1)
input_player_list.append(ppo2)
#input_player_list.append(ppo3)
input_player_list.append(ppo4)
print input_player_list

pgc.initGame(input_player_list)
pgc.runGame()
