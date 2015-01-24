#!/usr/bin/python

from HeadsUp import Card
from HandRanking import HandRanking
from PokerPlayerOpp import PokerPlayerOpp

ppOpponent = PokerPlayerOpp("Opponent", 0)
player_hand_dict = {}
player_hand_dict[ppOpponent.name] = []
handRanking = HandRanking([ppOpponent], player_hand_dict)

""" Straight flush test """
card_list_straight_flush = []
card_list_straight_flush.append(Card(3, 4))
card_list_straight_flush.append(Card(3, 5))
card_list_straight_flush.append(Card(3, 6))
card_list_straight_flush.append(Card(3, 7))
card_list_straight_flush.append(Card(3, 8))
assert handRanking.getRank(ppOpponent, card_list_straight_flush) == handRanking.RANK_STRAIGHT_FLUSH
card_list_straight_flush.append(Card(2, 4))
assert handRanking.getRank(ppOpponent, card_list_straight_flush) == handRanking.RANK_STRAIGHT_FLUSH
card_list_straight_flush.append(Card(0, 2))
assert handRanking.getRank(ppOpponent, card_list_straight_flush) == handRanking.RANK_STRAIGHT_FLUSH

""" Not straight flush test """
card_list_not_straight_flush = []
card_list_not_straight_flush.append(Card(3, 4))
card_list_not_straight_flush.append(Card(3, 6))
card_list_not_straight_flush.append(Card(3, 7))
card_list_not_straight_flush.append(Card(3, 8))
card_list_not_straight_flush.append(Card(2, 4))
assert handRanking.getRank(ppOpponent, card_list_not_straight_flush) != handRanking.RANK_STRAIGHT_FLUSH
card_list_not_straight_flush.append(Card(2, 5))
assert handRanking.getRank(ppOpponent, card_list_not_straight_flush) != handRanking.RANK_STRAIGHT_FLUSH
card_list_not_straight_flush.append(Card(0, 2))
assert handRanking.getRank(ppOpponent, card_list_not_straight_flush) != handRanking.RANK_STRAIGHT_FLUSH

""" Four of a kind test """
card_list_four_of_a_kind = []
card_list_four_of_a_kind.append(Card(2, 11))
card_list_four_of_a_kind.append(Card(3, 11))
card_list_four_of_a_kind.append(Card(1, 11))
card_list_four_of_a_kind.append(Card(0, 11))
card_list_four_of_a_kind.append(Card(0, 12))
assert handRanking.getRank(ppOpponent, card_list_four_of_a_kind) == handRanking.RANK_FOUR_OF_A_KIND
card_list_four_of_a_kind.append(Card(0, 13))
assert handRanking.getRank(ppOpponent, card_list_four_of_a_kind) == handRanking.RANK_FOUR_OF_A_KIND
card_list_four_of_a_kind.append(Card(1, 7))
assert handRanking.getRank(ppOpponent, card_list_four_of_a_kind) == handRanking.RANK_FOUR_OF_A_KIND

""" Not four of a kind test """
card_list_not_four_of_a_kind = []
card_list_not_four_of_a_kind.append(Card(2, 11))
card_list_not_four_of_a_kind.append(Card(3, 11))
card_list_not_four_of_a_kind.append(Card(1, 12))
card_list_not_four_of_a_kind.append(Card(0, 11))
card_list_not_four_of_a_kind.append(Card(0, 12))
assert handRanking.getRank(ppOpponent, card_list_not_four_of_a_kind) != handRanking.RANK_FOUR_OF_A_KIND
card_list_not_four_of_a_kind.append(Card(0, 13))
assert handRanking.getRank(ppOpponent, card_list_not_four_of_a_kind) != handRanking.RANK_FOUR_OF_A_KIND
card_list_not_four_of_a_kind.append(Card(1, 7))
assert handRanking.getRank(ppOpponent, card_list_not_four_of_a_kind) != handRanking.RANK_FOUR_OF_A_KIND

""" Full house test """
card_list_full_house = []
card_list_full_house.append(Card(2, 8))
card_list_full_house.append(Card(0, 8))
card_list_full_house.append(Card(3, 12))
card_list_full_house.append(Card(1, 12))
card_list_full_house.append(Card(0, 12))
assert handRanking.getRank(ppOpponent, card_list_full_house) == handRanking.RANK_FULL_HOUSE
card_list_full_house.append(Card(3, 13))
assert handRanking.getRank(ppOpponent, card_list_full_house) == handRanking.RANK_FULL_HOUSE
card_list_full_house.append(Card(1, 8))
assert handRanking.getRank(ppOpponent, card_list_full_house) == handRanking.RANK_FULL_HOUSE

""" Not full house test """
card_list_not_full_house = []
card_list_not_full_house.append(Card(2, 8))
card_list_not_full_house.append(Card(3, 12))
card_list_not_full_house.append(Card(1, 13))
card_list_not_full_house.append(Card(0, 12))
card_list_not_full_house.append(Card(3, 11))
assert handRanking.getRank(ppOpponent, card_list_not_full_house) != handRanking.RANK_FULL_HOUSE
card_list_not_full_house.append(Card(0, 11))
assert handRanking.getRank(ppOpponent, card_list_not_full_house) != handRanking.RANK_FULL_HOUSE
card_list_not_full_house.append(Card(1, 8))
assert handRanking.getRank(ppOpponent, card_list_not_full_house) != handRanking.RANK_FULL_HOUSE

""" Flush test """
card_list_flush = []
card_list_flush.append(Card(2, 8))
card_list_flush.append(Card(2, 7))
card_list_flush.append(Card(2, 10))
card_list_flush.append(Card(2, 12))
card_list_flush.append(Card(2, 14))
assert handRanking.getRank(ppOpponent, card_list_flush) == handRanking.RANK_FLUSH
card_list_flush.append(Card(3, 12))
assert handRanking.getRank(ppOpponent, card_list_flush) == handRanking.RANK_FLUSH
card_list_flush.append(Card(3, 13))
assert handRanking.getRank(ppOpponent, card_list_flush) == handRanking.RANK_FLUSH

""" Not flush test """
card_list_not_flush = []
card_list_not_flush.append(Card(2, 9))
card_list_not_flush.append(Card(3, 12))
card_list_not_flush.append(Card(2, 13))
card_list_not_flush.append(Card(2, 12))
card_list_not_flush.append(Card(3, 11))
assert handRanking.getRank(ppOpponent, card_list_not_flush) != handRanking.RANK_FLUSH
card_list_not_flush.append(Card(0, 9))
assert handRanking.getRank(ppOpponent, card_list_not_flush) != handRanking.RANK_FLUSH
card_list_not_flush.append(Card(2, 8))
assert handRanking.getRank(ppOpponent, card_list_not_flush) != handRanking.RANK_FLUSH

""" Straight test """
card_list_straight = []
card_list_straight.append(Card(2, 8))
card_list_straight.append(Card(3, 9))
card_list_straight.append(Card(2, 10))
card_list_straight.append(Card(1, 11))
card_list_straight.append(Card(3, 12))
assert handRanking.getRank(ppOpponent, card_list_straight) == handRanking.RANK_STRAIGHT
card_list_straight.append(Card(2, 5))
assert handRanking.getRank(ppOpponent, card_list_straight) == handRanking.RANK_STRAIGHT
card_list_straight.append(Card(2, 14))
assert handRanking.getRank(ppOpponent, card_list_straight) == handRanking.RANK_STRAIGHT

""" Not straight test """
card_list_not_straight = []
card_list_not_straight.append(Card(2, 9))
card_list_not_straight.append(Card(3, 10))
card_list_not_straight.append(Card(2, 11))
card_list_not_straight.append(Card(1, 12))
card_list_not_straight.append(Card(3, 7))
assert handRanking.getRank(ppOpponent, card_list_not_straight) != handRanking.RANK_STRAIGHT
card_list_not_straight.append(Card(0, 11))
assert handRanking.getRank(ppOpponent, card_list_not_straight) != handRanking.RANK_STRAIGHT
card_list_not_straight.append(Card(2, 14))
assert handRanking.getRank(ppOpponent, card_list_not_straight) != handRanking.RANK_STRAIGHT

""" Three of a kind test """
card_list_three_of_a_kind = []
card_list_three_of_a_kind.append(Card(2, 8))
card_list_three_of_a_kind.append(Card(3, 9))
card_list_three_of_a_kind.append(Card(2, 14))
card_list_three_of_a_kind.append(Card(1, 14))
card_list_three_of_a_kind.append(Card(3, 14))
assert handRanking.getRank(ppOpponent, card_list_three_of_a_kind) == handRanking.RANK_THREE_OF_A_KIND
card_list_three_of_a_kind.append(Card(2, 5))
assert handRanking.getRank(ppOpponent, card_list_three_of_a_kind) == handRanking.RANK_THREE_OF_A_KIND
card_list_three_of_a_kind.append(Card(2, 12))
assert handRanking.getRank(ppOpponent, card_list_three_of_a_kind) == handRanking.RANK_THREE_OF_A_KIND

""" Not three of a kind test """
card_list_not_three_of_a_kind = []
card_list_not_three_of_a_kind.append(Card(2, 9))
card_list_not_three_of_a_kind.append(Card(3, 9))
card_list_not_three_of_a_kind.append(Card(2, 11))
card_list_not_three_of_a_kind.append(Card(1, 11))
card_list_not_three_of_a_kind.append(Card(3, 7))
assert handRanking.getRank(ppOpponent, card_list_not_three_of_a_kind) != handRanking.RANK_THREE_OF_A_KIND
card_list_not_three_of_a_kind.append(Card(0, 7))
assert handRanking.getRank(ppOpponent, card_list_not_three_of_a_kind) != handRanking.RANK_THREE_OF_A_KIND
card_list_not_three_of_a_kind.append(Card(2, 12))
assert handRanking.getRank(ppOpponent, card_list_not_three_of_a_kind) != handRanking.RANK_THREE_OF_A_KIND

""" Two pair test """
card_list_two_pair = []
card_list_two_pair.append(Card(2, 8))
card_list_two_pair.append(Card(3, 9))
card_list_two_pair.append(Card(2, 14))
card_list_two_pair.append(Card(1, 14))
card_list_two_pair.append(Card(3, 8))
assert handRanking.getRank(ppOpponent, card_list_two_pair) == handRanking.RANK_TWO_PAIR
card_list_two_pair.append(Card(2, 5))
assert handRanking.getRank(ppOpponent, card_list_two_pair) == handRanking.RANK_TWO_PAIR
card_list_two_pair.append(Card(2, 12))
assert handRanking.getRank(ppOpponent, card_list_two_pair) == handRanking.RANK_TWO_PAIR

""" Not two pair test """
card_list_not_two_pair = []
card_list_not_two_pair.append(Card(2, 9))
card_list_not_two_pair.append(Card(3, 10))
card_list_not_two_pair.append(Card(2, 11))
card_list_not_two_pair.append(Card(1, 11))
card_list_not_two_pair.append(Card(3, 6))
assert handRanking.getRank(ppOpponent, card_list_not_two_pair) != handRanking.RANK_TWO_PAIR
card_list_not_two_pair.append(Card(0, 8))
assert handRanking.getRank(ppOpponent, card_list_not_two_pair) != handRanking.RANK_TWO_PAIR
card_list_not_two_pair.append(Card(2, 13))
assert handRanking.getRank(ppOpponent, card_list_not_two_pair) != handRanking.RANK_TWO_PAIR

""" Pair test """
card_list_pair = []
card_list_pair.append(Card(2, 14))
card_list_pair.append(Card(3, 9))
card_list_pair.append(Card(2, 2))
card_list_pair.append(Card(1, 2))
card_list_pair.append(Card(3, 8))
assert handRanking.getRank(ppOpponent, card_list_pair) == handRanking.RANK_PAIR
card_list_pair.append(Card(2, 5))
assert handRanking.getRank(ppOpponent, card_list_pair) == handRanking.RANK_PAIR
card_list_pair.append(Card(2, 12))
assert handRanking.getRank(ppOpponent, card_list_pair) == handRanking.RANK_PAIR

""" Not pair test """
card_list_not_pair = []
card_list_not_pair.append(Card(2, 9))
card_list_not_pair.append(Card(3, 10))
card_list_not_pair.append(Card(2, 11))
card_list_not_pair.append(Card(1, 12))
card_list_not_pair.append(Card(3, 6))
assert handRanking.getRank(ppOpponent, card_list_not_pair) != handRanking.RANK_PAIR
card_list_not_pair.append(Card(0, 7))
assert handRanking.getRank(ppOpponent, card_list_not_pair) != handRanking.RANK_PAIR
card_list_not_pair.append(Card(2, 14))
assert handRanking.getRank(ppOpponent, card_list_not_pair) != handRanking.RANK_PAIR

""" Extra test 1 """
card_list_extra_1 = []
card_list_extra_1.append(Card(2, 7))
card_list_extra_1.append(Card(0, 5))
card_list_extra_1.append(Card(3, 3))
card_list_extra_1.append(Card(0, 14))
card_list_extra_1.append(Card(1, 12))
card_list_extra_1.append(Card(0, 2))
card_list_extra_1.append(Card(1, 2))
assert handRanking.getRank(ppOpponent, card_list_extra_1) == handRanking.RANK_PAIR

""" Extra test 2 """
card_list_extra_2 = []
card_list_extra_2.append(Card(3, 2))
card_list_extra_2.append(Card(3, 5))
card_list_extra_2.append(Card(3, 3))
card_list_extra_2.append(Card(0, 14))
card_list_extra_2.append(Card(1, 12))
card_list_extra_2.append(Card(0, 2))
card_list_extra_2.append(Card(1, 2))
assert handRanking.getRank(ppOpponent, card_list_extra_2) == handRanking.RANK_THREE_OF_A_KIND

""" Extra test 3 """
card_list_extra_3 = []
card_list_extra_3.append(Card(1, 10))
card_list_extra_3.append(Card(2, 14))
card_list_extra_3.append(Card(1, 9))
card_list_extra_3.append(Card(0, 8))
card_list_extra_3.append(Card(2, 7))
card_list_extra_3.append(Card(1, 7))
card_list_extra_3.append(Card(0, 7))
assert handRanking.getRank(ppOpponent, card_list_extra_3) == handRanking.RANK_THREE_OF_A_KIND

print "Successeful!"
