from PokerPlayer import PokerPlayer
from PokerGame import PokerDecision

class PokerPlayerOpp(PokerPlayer):
  
    def __init__(self, name):
        super(PokerPlayerOpp, self).__init__(name)

    def getPokerDecision(self, game_state_list):
        if game_state_list[-1].chips_to_stay > game_state_list[-1].chips_bet_dict[self.name]:
            call_amount =  game_state_list[-1].chips_to_stay - game_state_list[-1].chips_bet_dict[self.name]
            return PokerDecision(self, PokerDecision.ACTION_TYPE_CALL, call_amount)
        else:
            return PokerDecision(self, PokerDecision.ACTION_TYPE_CHECK, 0)

