#!/usr/bin/python

#from PokerPlayer import PokerPlayer
from PokerPlayerJeff import *
from PokerPlayerOpp import *
from PokerGame import *

#ppj = PokerPlayerJeff("Jeff")
ppo1 = PokerPlayerOpp("Opponent 1")
ppo2 = PokerPlayerOpp("Opponent 2")

input_player_list = []
#input_player_list.append(ppj)
input_player_list.append(ppo1)
input_player_list.append(ppo2)
print input_player_list

pgc = PokerGameController(input_player_list, 1, 400)
pgc.initGame()
pgc.runGame()
