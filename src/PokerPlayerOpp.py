from PokerPlayer import PokerPlayer
from HeadsUp import PokerDecision

DEBUG = False
#DEBUG = True 

class PokerPlayerOpp(PokerPlayer):
  
    def __init__(self, name, pgc):
        super(PokerPlayerOpp, self).__init__(name, pgc)

    def getPokerDecision(self, game_state, decision_list):
        if DEBUG:
            print self.name + " making decision..."
            print "Sees chips_to_stay: " + str(game_state.chips_to_stay)
            print "I've bet          : " + str(game_state.chips_bet_dict[self.name])
            print "I have            : " + str(game_state.player_chips[self.name])
        #for decision in decision_list:
        #    print decision
        if game_state.chips_to_stay > game_state.chips_bet_dict[self.name] and game_state.chips_bet_dict[self.name] + game_state.player_chips[self.name] >= game_state.chips_to_stay:
            call_amount =  game_state.chips_to_stay - game_state.chips_bet_dict[self.name]
            return PokerDecision(self, PokerDecision.ACTION_TYPE_CALL, call_amount)
        elif game_state.chips_to_stay == game_state.chips_bet_dict[self.name]:
            return PokerDecision(self, PokerDecision.ACTION_TYPE_CHECK, 0)
        else:
            return PokerDecision(self, PokerDecision.ACTION_TYPE_FOLD, 0)

