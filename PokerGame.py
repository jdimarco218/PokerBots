import sys
import random
from HandRanking import HandRanking 
from Card import Card

SMALL_BLIND_AMOUNT = 100
BIG_BLIND_AMOUNT   = 200

random.seed ( 2 )

class PokerGameController(object):
    """
    " Manages the game.  This class holds the current game state,
    "     the history of game states, and the players.  
    "
    " Attributes:
    "     TODO
    "
    """

    BOARD_STATE_PRE_FLOP = 0
    BOARD_STATE_FLOP = 1
    BOARD_STATE_TURN = 2
    BOARD_STATE_RIVER = 3

    board_states = ["Pre-flop", "Flop", "Turn", "River"]

    def __init__(self, player_list, num_decks, starting_chips):
        self.player_list = player_list
        self.num_players = len(player_list)
        self.num_decks = num_decks
        self.starting_chips = starting_chips
        self.cards_per_hand = 2
        self.game_state_list = []
        self.player_order = []
        self.player_chips = {}
        self.player_hand_dict = {} 
        self.board_state = 0

    def initGame(self):
        """ Set a random ordering for players and initial Dealer """
        self.setPlayerOrder()
        self.game_state_list.append(PokerGameState(self.player_list, self.num_decks))
        self.dealer = 0
        self.board_state = 0

        """ Set the starting chips for all players """
        for player in self.player_order:
            self.player_chips[player.name] = self.starting_chips
        for player in self.player_order:
            print str(self.player_chips[player.name])

    """ TODO: handle running out of cards in the deck """
    def runGame(self):
        """ Init player hands to empty lists """
        for player in self.player_order:
            self.player_hand_dict[player.name] = []

        """ Deal the hand out starting with the player after the Dealer """
        self.dealCards(self.dealer)
        self.printPlayersHands()
        self.playHand()
        dealer = (self.dealer+1)%self.num_players

        """ Play until the termination conditions are met """
        if self.isGameFinished() == False:
            """ Increment dealer """
            self.dealer = (self.dealer+1)%self.num_players
            """ Push a new game state to the list """
            self.game_state_list.append(PokerGameState(self.player_list, self.num_decks))
            self.runGame()
        else:
            print "Game over!"

    def playHand(self):
        self.printGameState(self.game_state_list[-1])
        """ Set blind bets """
        if self.player_chips[self.player_list[(self.dealer+1)%self.num_players].name] >= BIG_BLIND_AMOUNT:
            betting_player = self.player_list[(self.dealer+1)%self.num_players]
            small_blind_decision = PokerDecision(betting_player, PokerDecision.ACTION_TYPE_RAISE, BIG_BLIND_AMOUNT)
            self.handleBet(betting_player, small_blind_decision, self.game_state_list[-1])
        if self.num_players > 2 and self.player_chips[self.player_list[(self.dealer+2)%self.num_players].name] >= SMALL_BLIND_AMOUNT:
            betting_player = self.player_list[(self.dealer+2)%self.num_players]
            small_blind_decision = PokerDecision(betting_player, PokerDecision.ACTION_TYPE_RAISE, SMALL_BLIND_AMOUNT)
            self.handleBet(betting_player, small_blind_decision, self.game_state_list[-1])

        self.board_state = 0
        """ Place bets for each round of cards on the board """
        while PokerGameController.board_states[self.board_state] != "River":
            self.printGameState(self.game_state_list[-1])
            self.placeBets()
            self.dealBoardCards()
            self.board_state = self.board_state + 1
        """ Play final round of the hand """
        self.printGameState(self.game_state_list[-1])
        self.placeBets()
        self.determineWinner()
        return

    def handleBet(self, player, poker_decision, poker_game_state):
        if self.player_chips[player.name] >= poker_decision.amount:
            if poker_game_state.chips_to_stay > poker_game_state.chips_bet_dict[player.name] + poker_decision.amount:
                """ Case: player didn't bet enough """
                print "Didn't bet enough!"
                sys.exit
            elif poker_decision.action_type == PokerDecision.ACTION_TYPE_RAISE:
                """ Case: player raised """
                print player.name + " raising " + str(poker_decision.amount) + "..."
                self.player_chips[player.name] -= poker_decision.amount 
                poker_game_state.chips_bet_dict[player.name] += poker_decision.amount
                poker_game_state.chips_to_stay = poker_game_state.chips_bet_dict[player.name] 
                poker_game_state.pot += poker_decision.amount
            elif poker_decision.action_type == PokerDecision.ACTION_TYPE_CALL:
                """ Case: player called """
                print player.name + " calling " + str(poker_decision.amount) + "..."
                self.player_chips[player.name] -= poker_decision.amount 
                poker_game_state.chips_bet_dict[player.name] += poker_decision.amount
                poker_game_state.chips_to_stay = poker_game_state.chips_bet_dict[player.name] 
                poker_game_state.pot += poker_decision.amount
            elif poker_decision.action_type == PokerDecision.ACTION_TYPE_CHECK:
                pass
        else:
            print "Player can't bet this much!"
            sys.exit

    """ TODO """
    def dealBoardCards(self):
        if self.board_state == PokerGameController.BOARD_STATE_PRE_FLOP:
            print "Flop..."
            """ Burn a card, then lay 3 """
            self.game_state_list[-1].deck.popCard()
            for card_num in range(3):
                self.game_state_list[-1].board.append(self.game_state_list[-1].deck.popCard())
        if self.board_state == PokerGameController.BOARD_STATE_FLOP:
            print "Turn..."
            """ Burn a card, then lay 1 """
            self.game_state_list[-1].deck.popCard()
            self.game_state_list[-1].board.append(self.game_state_list[-1].deck.popCard())
        if self.board_state == PokerGameController.BOARD_STATE_TURN:
            print "River..."
            """ Burn a card, then lay 1 """
            self.game_state_list[-1].deck.popCard()
            self.game_state_list[-1].board.append(self.game_state_list[-1].deck.popCard())
        if self.board_state == PokerGameController.BOARD_STATE_RIVER:
            """ TODO: handle this properly """
            print "Should never get here"

    def placeBets(self):
        current_final_decision = (self.dealer+1)%self.num_players 
        poker_decision = self.player_order[current_final_decision].getPokerDecision(self.game_state_list)
        """ TODO: validate poker_decision """
        current_turn = (current_final_decision + 1) % self.num_players
        while current_turn != current_final_decision:
            poker_decision = self.player_order[current_turn].getPokerDecision(self.game_state_list)
            """ TODO: validate poker_decision """
            """ TODO: update current_last_decision """
            self.handleDecision(poker_decision, self.game_state_list[-1])
            current_turn = (current_turn + 1) % self.num_players

    def handleDecision(self, poker_decision, curr_game_state):
        if poker_decision.action_type == PokerDecision.ACTION_TYPE_FOLD:
            """ TODO """
        elif poker_decision.action_type == PokerDecision.ACTION_TYPE_CHECK:
            if (poker_decision.amount != 0):
                print "Player decided to check, but sent amount: " + str(poker_decision.amount) + "!"
                sys.exit
            self.handleBet(poker_decision.decider, poker_decision, curr_game_state)
        elif poker_decision.action_type == PokerDecision.ACTION_TYPE_CALL:
            self.handleBet(poker_decision.decider, poker_decision, curr_game_state)
        elif poker_decision.action_type == PokerDecision.ACTION_TYPE_RAISE:
            """ TODO """
            """ update current_final_decision """
            pass
        else:
            print """ IDK HOW TO HANDLE """
            sys.exit

    """ TODO """
    def isGameFinished(self):
        """ Currently only if one player hits zero we terminate! """
        for player in self.player_list:
            if self.player_chips[player.name] <= 0:
                return True
        return False

    def setPlayerOrder(self):
        self.player_order = self.player_list
        random.shuffle(self.player_order)

    def dealCards(self, dealer):
        """ Deals the cards in round robin order, starting with the player after the Dealer """
        for card_num in range(self.cards_per_hand):
            for player in self.player_order[(dealer+1)%self.num_players:]+self.player_order[:(dealer+1)%self.num_players]:
                """ Consider most recent game_state at index -1 and deal one card """
                self.player_hand_dict[player.name].append(self.game_state_list[-1].deck.popCard())

    def printPlayersHands(self):
        print ""
        for player in self.player_order:
            print "Player " + player.name + "'s hand:"
            for i in range(len(self.player_hand_dict)):
                print self.player_hand_dict[player.name][i]
            print ""

    def printGameState(self, game_state):
        print ""
        print "#####  Current Game State #####"
        print "Pot: " + str(game_state.pot) + "   ",
        print "Chips to stay: " + str(game_state.chips_to_stay)
        for player in self.player_list:
            print "bet[" + player.name + "]: ",
            print game_state.chips_bet_dict[player.name],
            print "   chips[" + player.name + "]: ",
            print self.player_chips[player.name]
        print "Board: ",
        for card in game_state.board:
            print str(card) + " ",
        print ""

    """ TODO """
    def determineWinner(self):
        for player in self.player_list:
            for card in self.game_state_list[-1].board:
                self.player_hand_dict[player.name].append(Card(card.suit, card.rank))
        hand_ranking = HandRanking(self.player_list, self.player_hand_dict)
        hand_ranking.rankHands()
        winning_rank = -1
        winner = None
        tie_list = []
        """ Get winning rank """
        for player in self.player_list:
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
            print "found potential tie..."
            for player in tie_list:
                print player.name + "'s hand:"
                for card in hand_ranking.player_best_hand_dict[player.name]:
                    print card
            print "resolving tie..."
            result_tie_list = self.resolveTie(hand_ranking, tie_list)
            for player in result_tie_list:
                print player.name + ",",
            print " wins with",
            hand_ranking.printRanking(winning_rank)
            print "and takes " + str(self.game_state_list[-1].pot / len(tie_list)) + " chips!"
            for player in result_tie_list:
                self.player_chips[player.name] += self.game_state_list[-1].pot / len(tie_list)
        else:
            print winner.name + " wins with",
            hand_ranking.printRanking(winning_rank)
            print "and takes " + str(self.game_state_list[-1].pot) + " chips!"
            self.player_chips[winner.name] += self.game_state_list[-1].pot

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
    "     deck: cards left - shuffled initially
    "     pot: number of chips in play
    "     chips_bet_dict: dict of chips bet by each player so far 
    "     chips_to_stay: amount of chips needed to continue playing
    "     board: current cards on the board
    "
    """

    def __init__(self, player_list, num_decks):
        self.deck = Deck(num_decks)
        random.shuffle(self.deck.cards)
        self.pot = 0
        self.chips_bet_dict = {}
        for player in player_list:
            self.chips_bet_dict[player.name] = 0
        self.chips_to_stay = 0
        self.board = []
        self.num_raises = 0


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

