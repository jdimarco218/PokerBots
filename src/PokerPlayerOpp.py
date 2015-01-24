##
# Template module for Opponent's poker bot. Just fill out getPokerDecision()
##

import os

from PokerPlayer import PokerPlayer
from HeadsUp import PokerDecision

#DEBUG = False
DEBUG = True 

class PokerPlayerOpp(PokerPlayer):
  
    def __init__(self, name, pgc):
        super(PokerPlayerOpp, self).__init__(name, pgc)
        if os.path.isfile('./results/Opponent.txt'):
            os.remove('./results/Opponent.txt')

    def getPokerDecision(self, game_state, decision_list):
        file1 = open('results/Opponent.txt', 'a+')
        if DEBUG:
            file1.write("Making decision...\n")
            file1.write("Sees chips_to_stay: " + str(game_state.chips_to_stay) + "\n")
            file1.write("I've bet          : " + str(game_state.chips_bet_dict[self.name]) + "\n")
            file1.write("I have            : " + str(game_state.player_chips[self.name]) + "\n")
            file1.write("\n")

        if game_state.chips_to_stay > game_state.chips_bet_dict[self.name] and game_state.chips_bet_dict[self.name] + game_state.player_chips[self.name] >= game_state.chips_to_stay:
            call_amount =  game_state.chips_to_stay - game_state.chips_bet_dict[self.name]
            return PokerDecision(self, PokerDecision.ACTION_TYPE_CALL, call_amount)
        elif game_state.chips_to_stay == game_state.chips_bet_dict[self.name]:
            return PokerDecision(self, PokerDecision.ACTION_TYPE_CHECK, 0)
        else:
            return PokerDecision(self, PokerDecision.ACTION_TYPE_FOLD, 0)

