from Card import Card

class HandRanking(object):

    RANK_STRAIGHT_FLUSH = 8
    RANK_FOUR_OF_A_KIND = 7
    RANK_FULL_HOUSE = 6
    RANK_FLUSH = 5 
    RANK_STRAIGHT = 4
    RANK_THREE_OF_A_KIND = 3
    RANK_TWO_PAIR = 2
    RANK_PAIR = 1
    RANK_HIGH_CARD = 0

    TEXAS_HOLD_EM_COUNT = 7
    MIN_HAND_COUNT = 5

    def __init__(self, player_list, player_hand_dict):
        self.player_list = player_list
        self.player_ranks_dict = {}
        self.player_hand_dict = {}
        for player in self.player_list:
            self.player_ranks_dict[player.name] = 0
        self.player_best_hand_dict = {}
        if player_hand_dict:
            for player in self.player_list:
                self.player_hand_dict[player.name] = player_hand_dict[player.name]
        for player in self.player_list:
            self.player_best_hand_dict[player.name] = []


    def rankHands(self):
        """ Rank each player's hand first """
        for player in self.player_list:
            self.player_ranks_dict[player.name] = self.getRank(player, self.player_hand_dict[player.name])
        """ Check who has the highest rank """
        """ TODO """

    def getRank(self, player, card_list):
        card_list_len = len(card_list)
        if card_list_len < HandRanking.MIN_HAND_COUNT:
            print "Error: incorrect number of cards when ranking!"

        """ Check RANK_STRAIGHT_FLUSH """
        card_list.sort()
        """ Hand size is 5, so check the first card in each window of 5 """
        for i in range(card_list_len - 5, -1, -1):
            """ Begin with just the current card in list for this player's best hand """
            self.player_best_hand_dict[player.name] = []
            self.player_best_hand_dict[player.name].append(Card(card_list[i].suit, card_list[i].rank))
            """ Check for cards in a potential straight flush """
            num_matches = 0
            for j in range(1,5):
                if self.handContainsExact(card_list, card_list[i].suit, card_list[i].rank+j):
                    num_matches += 1
                    self.player_best_hand_dict[player.name].append(Card(card_list[i].suit, card_list[i].rank+j))
                else:
                    break
                if num_matches == 4:
                    return HandRanking.RANK_STRAIGHT_FLUSH

        """ Check RANK_FOUR_OF_A_KIND """
        card_list.sort()
        self.player_best_hand_dict[player.name] = []
        """ Don't need to check the last three cards since they would be matches """
        for i in range(card_list_len - 4, -1, -1):
            self.player_best_hand_dict[player.name] = []
            if (self.handContainsNumRank(card_list, card_list[i].rank) == 4):
                """ Add these four cards to the best hand """
                for j in range(4):
                    self.player_best_hand_dict[player.name].append(Card(card_list[i+j].suit, card_list[i].rank))
                """ Need to add one more card to the best 5 """
                for j in range(card_list_len - 1, -1, -1):
                    if card_list[j].rank != card_list[i].rank:
                        self.player_best_hand_dict[player.name].insert(0, Card(card_list[i-1].suit, card_list[i-1].rank))
                return HandRanking.RANK_FOUR_OF_A_KIND

        """ Check RANK_FULL_HOUSE """
        card_list.sort()
        self.player_best_hand_dict[player.name] = []
        """ If there is a full house, we need to search in reverse since there could be two sets of three """
        for i in range(card_list_len-1, -1, -1):
            """ Check for the three of a kind portion """
            full_house_three_of = 0
            full_house_two_of = 0
            if (self.handContainsNumRank(card_list, card_list[i].rank) == 3):
                full_house_three_of = card_list[i].rank
                """ Check for the pair portion starting from the back since there could be two pairs """
                for j in range(card_list_len-1, -1, -1):
                    """ Check >= 2 since there could be 3 of them """
                    if (self.handContainsNumRank(card_list, card_list[j].rank) >= 2 and card_list[j].rank != full_house_three_of):
                        full_house_two_of = card_list[j].rank
                        """ Found a full house - build hand and return """
                        num_added = 0
                        self.player_best_hand_dict[player.name] = []
                        for k in range(card_list_len):
                            if card_list[k].rank == full_house_three_of:
                                if num_added < 3:
                                    self.player_best_hand_dict[player.name].append(Card(card_list[k].suit, card_list[k].rank))
                                    num_added += 1
                        num_added = 0 
                        for k in range(card_list_len):
                            if card_list[k].rank == full_house_two_of:
                                if num_added < 2:
                                    self.player_best_hand_dict[player.name].insert(0, Card(card_list[k].suit, card_list[k].rank))
                                    num_added += 1
                        return HandRanking.RANK_FULL_HOUSE

        """ Check RANK_FLUSH """
        card_list.sort()
        self.player_best_hand_dict[player.name] = []
        if (self.handContainsNumSuit(card_list, 0) >=5):
            """ Check in reverse order to get highest ranks """
            num_added = 0
            for i in range(card_list_len-1, -1, -1):
                if card_list[i].suit == 0 and num_added < 5:
                    self.player_best_hand_dict[player.name].insert(0, Card(card_list[i].suit, card_list[i].rank))
            return HandRanking.RANK_FLUSH
        elif (self.handContainsNumSuit(card_list, 1) >=5):
            """ Check in reverse order to get highest ranks """
            num_added = 0
            for i in range(card_list_len-1, -1, -1):
                if card_list[i].suit == 1 and num_added < 5:
                    self.player_best_hand_dict[player.name].insert(0, Card(card_list[i].suit, card_list[i].rank))
            return HandRanking.RANK_FLUSH
        elif (self.handContainsNumSuit(card_list, 2) >=5):
            """ Check in reverse order to get highest ranks """
            num_added = 0
            for i in range(card_list_len-1, -1, -1):
                if card_list[i].suit == 2 and num_added < 5:
                    self.player_best_hand_dict[player.name].insert(0, Card(card_list[i].suit, card_list[i].rank))
            return HandRanking.RANK_FLUSH
        elif (self.handContainsNumSuit(card_list, 3) >=5):
            """ Check in reverse order to get highest ranks """
            num_added = 0
            for i in range(card_list_len-1, -1, -1):
                if card_list[i].suit == 3 and num_added < 5:
                    self.player_best_hand_dict[player.name].insert(0, Card(card_list[i].suit, card_list[i].rank))
            return HandRanking.RANK_FLUSH

        """ Check RANK_STRAIGHT """
        card_list.sort()
        self.player_best_hand_dict[player.name] = []
        """ TODO: account for low ace straight """
        """ Don't need to check the last four cards since they would be the end of the straight """
        for i in range(card_list_len - 5, -1, -1):
            self.player_best_hand_dict[player.name] = []
            self.player_best_hand_dict[player.name].append(Card(card_list[i].suit, card_list[i].rank))
            num_consecutive = 1
            """ Look for the next four cards in a potential straight """
            for j in range(card_list[i].rank+1, card_list[i].rank+5):
                if self.handContainsNumRank(card_list, j) >= 1:
                    temp_card = self.getCardAtRank(card_list, j)
                    if temp_card.rank == j:
                        self.player_best_hand_dict[player.name].append(Card(temp_card.suit, temp_card.rank))
                        num_consecutive += 1
            if num_consecutive >= 5:
                return HandRanking.RANK_STRAIGHT

        """ Check RANK_THREE_OF_A_KIND """
        card_list.sort()
        self.player_best_hand_dict[player.name] = []
        """ Don't need to check the last two cards since they would be included in a potential group of three """
        for i in range(card_list_len - 3, -1, -1):
            if self.handContainsNumRank(card_list, card_list[i].rank) >= 3:
                self.player_best_hand_dict[player.name] = []
                """ Find the rest of the three cards in the hand """
                for j in range(card_list_len):
                    if card_list[j].rank == card_list[i].rank:
                        self.player_best_hand_dict[player.name].append(Card(card_list[j].suit, card_list[j].rank))
                """ Find the two highest ranking remaining cards to use - search in reverse """
                num_added = 0
                for j in range(card_list_len-1, -1, -1):
                    if card_list[j].rank != card_list[i].rank:
                        """ Insert before the group of three for prioritization reasons """
                        self.player_best_hand_dict[player.name].insert(0, Card(card_list[j].suit, card_list[j].rank))
                        num_added += 1
                    if num_added >= 2:
                        return HandRanking.RANK_THREE_OF_A_KIND

        """ Check RANK_TWO_PAIR """
        card_list.sort()
        self.player_best_hand_dict[player.name] = []
        """ Don't need to check the last card since it would be included in one of the potential pairs """
        for i in range(card_list_len - 2, -1, -1):
            if self.handContainsNumRank(card_list, card_list[i].rank) >= 2:
                """ Found first pair. Save rank and search for another """
                pair_one_rank = card_list[i].rank
                for j in range(card_list_len - 2, -1, -1):
                    if self.handContainsNumRank(card_list, card_list[j].rank) >= 2 and card_list[j].rank != card_list[i].rank:
                        """ Found second unique pair. Build the hand """
                        pair_two_rank = card_list[j].rank
                        """ Add the two pairs for the first four cards """
                        for k in range(card_list_len):
                            if card_list[k].rank == pair_one_rank:
                                """ Add this card of one of the pairs either in front or behind """
                                if pair_one_rank > pair_two_rank:
                                    self.player_best_hand_dict[player.name].append(Card(card_list[k].suit, card_list[k].rank))
                                else:
                                    self.player_best_hand_dict[player.name].insert(0, Card(card_list[k].suit, card_list[k].rank))
                            if card_list[k].rank == pair_two_rank:
                                """ Add this card of one of the pairs either in front or behind """
                                if pair_two_rank > pair_one_rank:
                                    self.player_best_hand_dict[player.name].append(Card(card_list[k].suit, card_list[k].rank))
                                else:
                                    self.player_best_hand_dict[player.name].insert(0, Card(card_list[k].suit, card_list[k].rank))
                        """ Get the remaining highest ranking card for the kicker """
                        for k in range(card_list_len-1, -1, -1):
                            if card_list[k].rank != pair_one_rank and card_list[k].rank != pair_two_rank:
                                self.player_best_hand_dict[player.name].insert(0, Card(card_list[k].suit, card_list[k].rank))
                                return HandRanking.RANK_TWO_PAIR

        """ Check RANK_PAIR """
        card_list.sort()
        self.player_best_hand_dict[player.name] = []
        """ Don't need to check that last card since it would be included in the potential pair """
        for i in range(card_list_len - 2, -1, -1):
            if self.handContainsNumRank(card_list, card_list[i].rank) >= 2:
                """ Found a pair. Build the hand """
                self.player_best_hand_dict[player.name] = []
                for j in range(card_list_len):
                    if card_list[j].rank == card_list[i].rank:
                        """ Fill the pair """
                        self.player_best_hand_dict[player.name].append(Card(card_list[j].suit, card_list[j].rank))
                """ Fill in the remaining highest cards """
                num_added = 0
                for j in range(card_list_len-1, -1, -1):
                    if card_list[j].rank != card_list[i].rank:
                        self.player_best_hand_dict[player.name].insert(0, Card(card_list[j].suit, card_list[j].rank))
                        num_added += 1
                    if num_added >= 3:
                        return HandRanking.RANK_PAIR

        """ Check RANK_HIGH_CARD """
        card_list.sort()
        self.player_best_hand_dict[player.name] = []
        for i in range(card_list_len - 5, card_list_len):
            self.player_best_hand_dict[player.name].append(Card(card_list[i].suit, card_list[i].rank))
        return 0

    def getCardAtRank(self, card_list, rank):
        for card in card_list:
            if card.rank == rank:
                return card 

    def handContainsExact(self, card_list, suit, rank):
        for card in card_list:
            if card.rank == rank and card.suit == suit:
                return True
        return False

    def handContainsNumRank(self, card_list, rank):
        num_at_rank = 0
        for card in card_list:
            if card.rank == rank:
                num_at_rank += 1
        return num_at_rank

    def handContainsNumSuit(self, card_list, suitNum):
        num_at_suit = 0
        for card in card_list:
            if card.suit == suitNum:
                num_at_suit += 1
        return num_at_suit

    def printRanking(self, rank_num):
        if rank_num == self.RANK_HIGH_CARD:
            print "High Card",
        elif rank_num == self.RANK_PAIR:
            print "Pair",
        elif rank_num == self.RANK_TWO_PAIR:
            print "Two pair",
        elif rank_num == self.RANK_THREE_OF_A_KIND:
            print "Three of a kind",
        elif rank_num == self.RANK_STRAIGHT:
            print "Straight",
        elif rank_num == self.RANK_FLUSH:
            print "Flush",
        elif rank_num == self.RANK_FULL_HOUSE:
            print "Full house",
        elif rank_num == self.RANK_FOUR_OF_A_KIND:
            print "Four of a kind",
        elif rank_num == self.RANK_STRAIGHT_FLUSH:
            print "Straight flush",
        return
