##
# Jeff's poker bot. Behold the best poker strategy ever!
# December 2014
##

import os

from PokerPlayer import PokerPlayer
from HeadsUp   import PokerGameState
from HeadsUp   import PokerDecision
from HandRanking import HandRanking
from Card        import Card

#DEBUG = False
DEBUG = True

# File location for output
dirPath = os.path.dirname(os.path.realpath(__file__))
relativeResultsPath = '/../results/Jeff.txt'
resultsPath = dirPath + relativeResultsPath

class PokerPlayerJeff(PokerPlayer):

  
    def __init__(self, name, pgc):
        super(PokerPlayerJeff, self).__init__(name, pgc)
        if os.path.isfile(resultsPath):
            os.remove(resultsPath)
        self.myHandDict = {}
        self.myHandDict[self.name] = [] 
        self.myHandRanking = HandRanking([self], self.myHandDict)

    def getPokerDecision(self, game_state, decision_list):
        file1 = open(resultsPath, 'a+')
        print self.name + " making decision..."
        if DEBUG: 
            file1.write("Sees chips_to_stay: " + str(game_state.chips_to_stay) + "\n")
            file1.write("I've bet          : " + str(game_state.chips_bet_dict[self.name]) + "\n")
            file1.write("I have            : " + str(game_state.player_chips[self.name]) + "\n")
            file1.write("\n")

        isPair = self.hand[0].rank == self.hand[1].rank
        if game_state.chips_to_stay > game_state.chips_bet_dict[self.name] + game_state.player_chips[self.name]:
            """ Need to fold, cannot play """
            return PokerDecision(self, PokerDecision.ACTION_TYPE_FOLD, 0)
        elif game_state.chips_to_stay > game_state.chips_bet_dict[self.name] and game_state.chips_bet_dict[self.name] + game_state.player_chips[self.name] >= game_state.chips_to_stay:
            if PokerGameState.board_states[game_state.board_state] == "Pre-flop":
                """ Determine fold conditions """
                sum = self.hand[0].rank + self.hand[1].rank 
                if sum < 14 and not isPair:
                    if DEBUG:
                        file1.write("Folding pre-flop because low ranks and no pair...")
                    return PokerDecision(self, PokerDecision.ACTION_TYPE_FOLD, 0)
                if isPair and game_state.player_chips[self.name] >= 500: 
                    return PokerDecision(self, PokerDecision.ACTION_TYPE_RAISE, 500)
                    if DEBUG:
                        file1.write("Raising pre-flop because pair...")
                call_amount =  game_state.chips_to_stay - game_state.chips_bet_dict[self.name]
                return PokerDecision(self, PokerDecision.ACTION_TYPE_CALL, call_amount)
            elif PokerGameState.board_states[game_state.board_state] == "Flop" or PokerGameState.board_states[game_state.board_state] == "Turn" or PokerGameState.board_states[game_state.board_state] == "River":
                tempCardList = []
                for card in self.hand:
                    tempCardList.append(Card(card.suit, card.rank))
                for card in game_state.board:
                    tempCardList.append(Card(card.suit, card.rank))
                tempRanking = self.myHandRanking.getRank(self, tempCardList)
                if DEBUG:
                    file1.write("Ranking: " + str(tempRanking))
                if tempRanking >= HandRanking.RANK_THREE_OF_A_KIND:
                    if game_state.player_chips[self.name] - game_state.chips_bet_dict[self.name] > 0:
                        return PokerDecision(self, PokerDecision.ACTION_TYPE_RAISE, game_state.player_chips[self.name])
                    else:
                        return PokerDecision(self, PokerDecision.ACTION_TYPE_CHECK, 0)
                call_amount =  game_state.chips_to_stay - game_state.chips_bet_dict[self.name]
                return PokerDecision(self, PokerDecision.ACTION_TYPE_CALL, call_amount)
            else:
                call_amount =  game_state.chips_to_stay - game_state.chips_bet_dict[self.name]
                return PokerDecision(self, PokerDecision.ACTION_TYPE_CALL, call_amount)
        else:
            if PokerGameState.board_states[game_state.board_state] == "Flop" or PokerGameState.board_states[game_state.board_state] == "Turn" or PokerGameState.board_states[game_state.board_state] == "River":
                tempCardList = []
                for card in self.hand:
                    tempCardList.append(Card(card.suit, card.rank))
                for card in game_state.board:
                    tempCardList.append(Card(card.suit, card.rank))
                tempRanking = self.myHandRanking.getRank(self, tempCardList)
                if DEBUG:
                    file1.write("Ranking: " + str(tempRanking))
                if tempRanking >= HandRanking.RANK_THREE_OF_A_KIND:
                    if game_state.player_chips[self.name] - game_state.chips_bet_dict[self.name] > 0:
                        """ Bet 500 if available """
                        if game_state.player_chips[self.name] >= 500:
                            return PokerDecision(self, PokerDecision.ACTION_TYPE_RAISE, 500)
                    else:
                        return PokerDecision(self, PokerDecision.ACTION_TYPE_CHECK, 0)
                return PokerDecision(self, PokerDecision.ACTION_TYPE_CHECK, 0)
            return PokerDecision(self, PokerDecision.ACTION_TYPE_CHECK, 0)

