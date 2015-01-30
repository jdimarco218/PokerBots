import sys
import random
from HandRanking import HandRanking 
from Card import Card

CARDS_PER_PLAYER   = 2
SMALL_BLIND_AMOUNT = 100
BIG_BLIND_AMOUNT   = 200

#DEBUG = True
DEBUG = False

random.seed ( 1 )

class PokerGameController(object):
    """
    " Manages the game.  This class holds the current game state,
    "     the history of game states, and the players.  
    "
    " Attributes:
    "     TODO
    "
    """

    def __init__(self, num_decks, starting_chips):
        self.player_list = []
        self.dealer = 0
        self.starting_chips = starting_chips
        self.player_chips = {}
        self.decision_list = []
        self.player_hand_dict = {} 
        self.num_players = 2

    def initGame(self, player_list):
        self.player_list = player_list
        self.game_state = PokerGameState(self.player_list, self.starting_chips)

    """ TODO: handle running out of cards in the deck """
    def runGame(self):
        """ Init player hands to empty lists """
        for player in self.game_state.player_list:
            self.player_hand_dict[player.name] = []

        """ Deal the hand out starting with the player after the Dealer """
        print "Dealing cards..."
        self.dealCards(self.dealer)
        self.printPlayersHands()
        self.playHand()
        dealer = (self.dealer+1)%self.num_players

        """ Play until the termination conditions are met """
        if self.isGameFinished() == False:
            """ Increment dealer """
            self.dealer = (self.dealer+1)%self.num_players
            """ Reset the game state """
            self.game_state.newGameState()
            self.decision_list = []
            self.runGame()
        else:
            print ""
            print "Game over!"

    def playHand(self):
        self.printGameState(self.game_state)
        """ Set blind bets """
        """ Big blind needs to be issued after the small blind since chips_to_stay would be too large otherwise """
        """ Small blind """
        if self.game_state.player_chips[self.game_state.player_list[self.dealer].name] >= SMALL_BLIND_AMOUNT:
            betting_player = self.game_state.player_list[self.dealer]
            small_blind_decision = PokerDecision(betting_player, PokerDecision.ACTION_TYPE_RAISE, SMALL_BLIND_AMOUNT)
            self.handleDecision(small_blind_decision)
        else:
            print "Error: " + str(self.game_state.player_list[self.dealer].name) + " doesn't have enough chips for the small blind!"
            sys.exit
        if self.game_state.player_chips[self.game_state.player_list[(self.dealer+1)%self.num_players].name] >= BIG_BLIND_AMOUNT:
            """ Big blind """
            betting_player = self.game_state.player_list[(self.dealer+1)%self.num_players]
            big_blind_decision = PokerDecision(betting_player, PokerDecision.ACTION_TYPE_RAISE, BIG_BLIND_AMOUNT)
            self.handleDecision(big_blind_decision)
        else:
            print "Error: " + str(self.game_state.player_list[(self.dealer+1)%self.num_players].name) + " doesn't have enough chips for the big blind!"
            sys.exit

        self.game_stateboard_state = 0
        """ Place bets for each round of cards on the board """
        while PokerGameState.board_states[self.game_state.board_state] != "River":
            self.printGameState(self.game_state)
            self.placeBets()
            if self.game_state.numActive() == 1:
                """ Players folded """
                self.determineWinner()
                return
            self.dealBoardCards()
            self.game_state.board_state = self.game_state.board_state + 1
        """ Play final round of the hand """
        self.printGameState(self.game_state)
        self.placeBets()
        self.determineWinner()
        return

    def handleBet(self, player, poker_decision, poker_game_state):
        if self.game_state.player_chips[player.name] >= poker_decision.amount:
            if poker_game_state.chips_to_stay > poker_game_state.chips_bet_dict[player.name] + poker_decision.amount:
                """ Case: player didn't bet enough """
                print "Error: Player didn't bet enough!" 
                print "chips_to_stay: " + str(poker_game_state.chips_to_stay) + "  vs bet: " + str(poker_game_state.chips_bet_dict[player.name] + poker_decision.amount)
                sys.exit
            elif poker_decision.action_type == PokerDecision.ACTION_TYPE_RAISE:
                """ Case: player raised """
                self.game_state.player_chips[player.name] -= poker_decision.amount 
                poker_game_state.chips_bet_dict[player.name] += poker_decision.amount
                poker_game_state.chips_to_stay = poker_game_state.chips_bet_dict[player.name] 
                poker_game_state.pot += poker_decision.amount
            elif poker_decision.action_type == PokerDecision.ACTION_TYPE_CALL:
                """ Case: player called """
                self.game_state.player_chips[player.name] -= poker_decision.amount 
                poker_game_state.chips_bet_dict[player.name] += poker_decision.amount
                poker_game_state.chips_to_stay = poker_game_state.chips_bet_dict[player.name] 
                poker_game_state.pot += poker_decision.amount
            elif poker_decision.action_type == PokerDecision.ACTION_TYPE_CHECK:
                pass
        else:
            print "Error: Player can't bet this much! (" + str(poker_decision.amount) + " vs " + str(self.player_chips[poker_decision.decider.name])
            sys.exit

    """ TODO """
    def dealBoardCards(self):
        if self.game_state.board_state == PokerGameState.BOARD_STATE_PRE_FLOP:
            print ""
            print "Flop..."
            """ Burn a card, then lay 3 """
            self.game_state.deck.popCard()
            for card_num in range(3):
                self.game_state.board.append(self.game_state.deck.popCard())
        if self.game_state.board_state == PokerGameState.BOARD_STATE_FLOP:
            print "Turn..."
            """ Burn a card, then lay 1 """
            self.game_state.deck.popCard()
            self.game_state.board.append(self.game_state.deck.popCard())
        if self.game_state.board_state == PokerGameState.BOARD_STATE_TURN:
            print "River..."
            """ Burn a card, then lay 1 """
            self.game_state.deck.popCard()
            self.game_state.board.append(self.game_state.deck.popCard())
        if self.game_state.board_state == PokerGameState.BOARD_STATE_RIVER:
            """ TODO: handle this properly """
            print "Error: Cannot deal cards during river state! Should never get here"
            sys.exit

    def placeBets(self):
        """ Determine who goes first """
        if self.game_state.board_state == PokerGameState.BOARD_STATE_PRE_FLOP:
            self.game_state.current_turn_index = self.dealer
            self.game_state.current_final_decision_index = self.game_state.current_turn_index
        else:
            self.game_state.current_turn_index = (self.dealer+1)%self.num_players
            self.game_state.current_final_decision_index = self.game_state.current_turn_index
        if DEBUG:
            print "current_final_decision_index: " + str(self.game_state.current_final_decision_index) + "  " + str(self.game_state.player_list[self.game_state.current_final_decision_index].name)
            print "current_turn_index: " + str(self.game_state.current_turn_index) + "  " + str(self.game_state.player_list[self.game_state.current_turn_index].name)

        """ Run an initial decision so that current_turn_index doesn't equal current_final_decision_index """
        if DEBUG:
            print "Getting initial poker decision from " + str(self.game_state.player_list[self.game_state.current_turn_index].name)
        poker_decision = self.game_state.player_list[self.game_state.current_turn_index].getPokerDecision(self.game_state, self.decision_list)
        self.handleDecision(poker_decision)
        self.game_state.current_turn_index = (self.game_state.current_turn_index + 1) % self.num_players
        if DEBUG:
            print "current_turn_index: " + str(self.game_state.current_turn_index) + "  " + str(self.game_state.player_list[self.game_state.current_turn_index].name)
            print "current_final_decision_index: " + str(self.game_state.current_final_decision_index) + "  " + str(self.game_state.player_list[self.game_state.current_final_decision_index].name)

        while int(self.game_state.current_turn_index) != int(self.game_state.current_final_decision_index):
            if self.game_state.numActive() == 1:
                return
            if DEBUG:
                print "Getting poker decision from " + str(self.game_state.player_list[self.game_state.current_turn_index].name) + "..."
            poker_decision = self.game_state.player_list[self.game_state.current_turn_index].getPokerDecision(self.game_state, self.decision_list)
            self.handleDecision(poker_decision)
            self.game_state.current_turn_index = (self.game_state.current_turn_index + 1) % self.num_players
            if poker_decision.action_type == PokerDecision.ACTION_TYPE_RAISE:
                self.game_state.current_final_decision_index = self.game_state.current_turn_index
            if DEBUG:
                print "Next current_turn_index: " + str(self.game_state.current_turn_index) + "  " + str(self.game_state.player_list[self.game_state.current_turn_index].name)
                print "Next current_final_decision_index: " + str(self.game_state.current_final_decision_index) + "  " + str(self.game_state.player_list[self.game_state.current_final_decision_index].name)
                print "while() cond: " + str(int(self.game_state.current_turn_index) != int(self.game_state.current_final_decision_index))

    def handleDecision(self, poker_decision):
        if poker_decision.action_type == PokerDecision.ACTION_TYPE_FOLD:
            print poker_decision.decider.name + " folding "
            self.game_state.active_dict[poker_decision.decider.name] = False
            """ Add to decision_list """
            self.decision_list.append(poker_decision)
            """ Check if out of chips """
            if self.game_state.player_chips[poker_decision.decider.name] < BIG_BLIND_AMOUNT: 
                if DEBUG:
                    print poker_decision.decider.name + " has run out of chips! Eliminated!"
        elif poker_decision.action_type == PokerDecision.ACTION_TYPE_CHECK:
            print poker_decision.decider.name + " checking "
            if (poker_decision.amount != 0):
                print "Error: Player decided to check, but sent amount: " + str(poker_decision.amount) + "!"
                sys.exit
            self.handleBet(poker_decision.decider, poker_decision, self.game_state)
            """ Add to decision_list """
            self.decision_list.append(poker_decision)
        elif poker_decision.action_type == PokerDecision.ACTION_TYPE_CALL:
            print poker_decision.decider.name + " calling " + str(poker_decision.amount)
            self.handleBet(poker_decision.decider, poker_decision, self.game_state)
            """ Add to decision_list """
            self.decision_list.append(poker_decision)
        elif poker_decision.action_type == PokerDecision.ACTION_TYPE_RAISE:
            print poker_decision.decider.name + " raising " + str(poker_decision.amount)
            self.handleBet(poker_decision.decider, poker_decision, self.game_state)
            self.game_state.num_raises += 1
            """ Add to decision_list """
            self.decision_list.append(poker_decision)
        else:
            print "Error: Unknown decision type."
            sys.exit

    """ TODO """
    def isGameFinished(self):
        #if self.num_players == 1:
        #    return True
        for player in self.game_state.player_list:
            if self.game_state.player_chips[player.name] < BIG_BLIND_AMOUNT:
                return True
        return False

    def dealCards(self, dealer):
        """ Deals the cards in round robin order, starting with the player after the Dealer """
        for card_num in range(CARDS_PER_PLAYER):
            for player in self.game_state.player_list[(dealer+1)%self.num_players:]+self.game_state.player_list[:(dealer+1)%self.num_players]:
                """ Deal one card """
                self.player_hand_dict[player.name].append(self.game_state.deck.popCard())
        for player in self.game_state.player_list:
            player.hand = self.player_hand_dict[player.name]

    def printPlayersHands(self):
        print ""
        for player in self.game_state.player_list:
            print "Player " + player.name + "'s hand:"
            for i in range(len(self.player_hand_dict[player.name])):
                print self.player_hand_dict[player.name][i]
            print ""

    def printGameState(self, game_state):
        print ""
        print "#####  Current Game State #####"
        print "Dealer: " + str(game_state.player_list[self.dealer].name)
        print "Num Active: " + str(game_state.numActive())
        print "Pot: " + str(game_state.pot) + "   ",
        print "Chips to stay: " + str(game_state.chips_to_stay)
        for player in self.game_state.player_list:
            print "bet[" + player.name + "]: ",
            print game_state.chips_bet_dict[player.name],
            print "   chips[" + player.name + "]: ",
            print game_state.player_chips[player.name]
        print "Board: ",
        for card in game_state.board:
            print str(card) + " ",
        print ""

    """ TODO """
    def determineWinner(self):
        """ Check if only one player active """
        if self.game_state.numActive() == 1:
            for player in self.game_state.player_list:
                if self.game_state.active_dict[player.name]:
                    print ""
                    print player.name + " wins with"
                    for card in self.player_hand_dict[player.name]:
                        print card
                    print "and takes " + str(self.game_state.pot) + " chips!"
                    self.game_state.player_chips[player.name] += self.game_state.pot
                    return

        for player in self.game_state.player_list:
            for card in self.game_state.board:
                self.player_hand_dict[player.name].append(Card(card.suit, card.rank))
        hand_ranking = HandRanking(self.game_state.player_list, self.player_hand_dict)
        hand_ranking.rankHands()
        winning_rank = -1
        winner = None
        tie_list = []
        """ Get winning rank, only consider active players for the pot """
        for player in self.game_state.player_list:
            if self.game_state.active_dict[player.name] == True:
                if DEBUG:
                    print "Considering " + str(player.name) + "'s hand for the pot."
                if hand_ranking.player_ranks_dict[player.name] > winning_rank:
                    winning_rank = hand_ranking.player_ranks_dict[player.name]
                    winner = player    
                    tie_list = []
                    tie_list.append(player)
                elif hand_ranking.player_ranks_dict[player.name] == winning_rank:
                    tie_list.append(player)
        """ winner should never be equal to None """

        """ Check for tie and resolve if needed """
        if len(tie_list) > 1:
            if DEBUG:
                print "found potential tie..."
                for player in tie_list:
                    print player.name + "'s hand:"
                    for card in hand_ranking.player_best_hand_dict[player.name]:
                        print card
                print "resolving tie..."
            result_tie_list = self.resolveTie(hand_ranking, tie_list)
            print ""
            self.printPlayersHands()
            for player in result_tie_list:
                print player.name + ",",
            print " wins with",
            hand_ranking.printRanking(winning_rank)
            print "and takes " + str(self.game_state.pot / len(tie_list)) + " chips!"
            for player in result_tie_list:
                self.game_state.player_chips[player.name] += self.game_state.pot / len(tie_list)
        else:
            print ""
            self.printPlayersHands()
            print winner.name + " wins with",
            hand_ranking.printRanking(winning_rank)
            print "and takes " + str(self.game_state.pot) + " chips!"
            self.game_state.player_chips[winner.name] += self.game_state.pot

    """ TODO """
    def resolveTie(self, hand_ranking, tie_list):
        """ Get max at each index """
        max_rank_list = [] 

        for i in range(5):
            """ Lowest rank card as baseline """
            curr_max_rank = 0 
            for player in tie_list:
                if hand_ranking.player_best_hand_dict[player.name][i].rank > curr_max_rank:
                    curr_max_rank = hand_ranking.player_best_hand_dict[player.name][i].rank
            max_rank_list.append(curr_max_rank)

        """ Compare player hands to max_rank_list """
        """ Start with final card and loop towards lowest rank """
        for i in range(5-1, -1, -1):
            for player in tie_list:
                if hand_ranking.player_best_hand_dict[player.name][i].rank < max_rank_list[i] and len(tie_list) > 1:
                    tie_list.remove(player)
        return tie_list


class PokerGameState(object):
    """
    " Represents the current state of the game.
    "
    " Attributes:
    "     TODO: update rest
    "     deck: cards left - shuffled initially
    "     pot: number of chips in play
    "     chips_bet_dict: dict of chips bet by each player so far 
    "     chips_to_stay: amount of chips needed to continue playing
    "     board: current cards on the board
    "
    """

    BOARD_STATE_PRE_FLOP = 0
    BOARD_STATE_FLOP = 1
    BOARD_STATE_TURN = 2
    BOARD_STATE_RIVER = 3

    board_states = ["Pre-flop", "Flop", "Turn", "River"]

    def __init__(self, player_list, starting_chips):
        self.deck = Deck(1)
        random.shuffle(self.deck.cards)
        self.player_list = player_list
        self.player_chips = {} 
        self.setPlayerOrder()
        """ Set the starting chips for all players """
        for player in self.player_list:
            self.player_chips[player.name] = starting_chips
        for player in self.player_list:
            print str(self.player_chips[player.name])
        self.pot = 0
        self.chips_bet_dict = {}
        self.active_dict = {}
        for player in player_list:
            self.chips_bet_dict[player.name] = 0
        for player in player_list:
            self.active_dict[player.name] = True
        self.chips_to_stay = 0
        self.board = []
        self.board_state = 0
        self.num_raises = 0
        self.current_final_decision_index = 0
        self.current_turn_index = 0

    def newGameState(self):
        self.deck = Deck(1)
        random.shuffle(self.deck.cards)
        self.pot = 0
        for player in self.player_list:
            self.chips_bet_dict[player.name] = 0
        for player in self.player_list:
            self.active_dict[player.name] = True
        self.chips_to_stay = 0
        self.board = []
        self.board_state = 0
        self.num_raises = 0
        self.current_final_decision_index = 0

    def setPlayerOrder(self):
        random.shuffle(self.player_list)
        
    def numActive(self):
        result = 0
        for player in self.player_list:
            if self.active_dict[player.name]:
                result += 1
        return result


class PokerDecision(object):
    """
    " Represents a decision made by a player given the current state
    "
    " Attributes:
    "     TODO
    """
    ACTION_TYPE_FOLD = 0
    ACTION_TYPE_CHECK = 1
    ACTION_TYPE_CALL = 2
    ACTION_TYPE_RAISE = 3

    action_types = ["Fold", "Check", "Call", "Raise"]

    def __init__(self, decider, action_type, amount=0):
        self.decider = decider
        self.action_type = action_type
        self.amount = amount

    def __str__(self):
        res = []
        res.append("## Poker Decision ##")
        res.append("-- " + str(self.decider.name) + " " + str(self.action_types[self.action_type]) + "s " + str(self.amount))
        return '\n'.join(res)


class Deck(object):
    """
    " Represents a deck of standard playing cards.
    "
    " Attributes:
    "     cards: list of playing cards
    """

    def __init__(self, num_decks):
        self.cards = []
        for deck in range(num_decks):
            for suit in range(4):
                for rank in range(2, 15):
                    card = Card(suit, rank)
                    self.cards.append(card)

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)

    def shuffle(self):
        """ Shuffles the cards in this deck. """
        random.shuffle(self.cards)

    def popCard(self, i=0):
        """  Removes and returns a card from the deck. First card default"""
        return self.cards.pop(i)
