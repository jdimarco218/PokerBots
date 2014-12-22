from PokerPlayer import PokerPlayer
from PokerGame import PokerDecision

class PokerPlayerAllInBot(PokerPlayer):
  
    def __init__(self, name, pgc):
        super(PokerPlayerAllInBot, self).__init__(name, pgc)

    def getPokerDecision(self, game_state, decision_list):
        if game_state.player_chips[self.name] > 0:
            return PokerDecision(self, PokerDecision.ACTION_TYPE_RAISE, game_state.player_chips[self.name])
        else:
            return PokerDecision(self, PokerDecision.ACTION_TYPE_CHECK, 0)

