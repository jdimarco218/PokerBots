from HeadsUp import PokerGameState

class PokerPlayer(object):
    def __init__(self, name, pgc):
        self.name = name
        self.pgc  = pgc
        self.hand = []

    def getPokerDecision(self, game_state, decision_list):
        return False
