#!/usr/bin/python

from PokerGame import Card
from HandRanking import HandRanking
from PokerPlayerOpp import PokerPlayerOpp

ppo1 = PokerPlayerOpp("Opponent 1")
hr1 = HandRanking([], {})

""" Straight flush test """
card_list_straight_flush = []
card_list_straight_flush.append(Card(3, 4))
card_list_straight_flush.append(Card(3, 5))
card_list_straight_flush.append(Card(3, 6))
card_list_straight_flush.append(Card(2, 4))
card_list_straight_flush.append(Card(3, 7))
card_list_straight_flush.append(Card(3, 8))
card_list_straight_flush.append(Card(0, 2))
assert hr1.getRank(ppo1, card_list_straight_flush) == hr1.RANK_STRAIGHT_FLUSH

""" Not straight flush test """
card_list_not_straight_flush = []
card_list_not_straight_flush.append(Card(3, 4))
card_list_not_straight_flush.append(Card(2, 5))
card_list_not_straight_flush.append(Card(3, 6))
card_list_not_straight_flush.append(Card(2, 4))
card_list_not_straight_flush.append(Card(3, 7))
card_list_not_straight_flush.append(Card(3, 8))
card_list_not_straight_flush.append(Card(0, 2))
assert hr1.getRank(ppo1, card_list_not_straight_flush) != hr1.RANK_STRAIGHT_FLUSH

""" Four of a kind test """
card_list_four_of_a_kind = []
card_list_four_of_a_kind.append(Card(2, 11))
card_list_four_of_a_kind.append(Card(3, 11))
card_list_four_of_a_kind.append(Card(1, 11))
card_list_four_of_a_kind.append(Card(0, 11))
card_list_four_of_a_kind.append(Card(0, 12))
card_list_four_of_a_kind.append(Card(0, 13))
card_list_four_of_a_kind.append(Card(1, 7))
assert hr1.getRank(ppo1, card_list_four_of_a_kind) == hr1.RANK_FOUR_OF_A_KIND

""" Not four of a kind test """
card_list_not_four_of_a_kind = []
card_list_not_four_of_a_kind.append(Card(2, 11))
card_list_not_four_of_a_kind.append(Card(3, 11))
card_list_not_four_of_a_kind.append(Card(1, 12))
card_list_not_four_of_a_kind.append(Card(0, 11))
card_list_not_four_of_a_kind.append(Card(0, 12))
card_list_not_four_of_a_kind.append(Card(0, 13))
card_list_not_four_of_a_kind.append(Card(1, 7))
assert hr1.getRank(ppo1, card_list_not_four_of_a_kind) != hr1.RANK_FOUR_OF_A_KIND

""" Full house test """
card_list_full_house = []
card_list_full_house.append(Card(2, 8))
card_list_full_house.append(Card(3, 12))
card_list_full_house.append(Card(1, 12))
card_list_full_house.append(Card(0, 12))
card_list_full_house.append(Card(3, 13))
card_list_full_house.append(Card(0, 8))
card_list_full_house.append(Card(1, 8))
assert hr1.getRank(ppo1, card_list_full_house) == hr1.RANK_FULL_HOUSE

""" Not full house test """
card_list_not_full_house = []
card_list_not_full_house.append(Card(2, 8))
card_list_not_full_house.append(Card(3, 12))
card_list_not_full_house.append(Card(1, 13))
card_list_not_full_house.append(Card(0, 12))
card_list_not_full_house.append(Card(3, 11))
card_list_not_full_house.append(Card(0, 11))
card_list_not_full_house.append(Card(1, 8))
assert hr1.getRank(ppo1, card_list_not_full_house) != hr1.RANK_FULL_HOUSE

""" Full house test """
card_list_flush = []
card_list_flush.append(Card(2, 8))
card_list_flush.append(Card(3, 12))
card_list_flush.append(Card(2, 12))
card_list_flush.append(Card(2, 14))
card_list_flush.append(Card(3, 13))
card_list_flush.append(Card(2, 7))
card_list_flush.append(Card(2, 10))
assert hr1.getRank(ppo1, card_list_flush) == hr1.RANK_FLUSH

""" Not full house test """
card_list_not_flush = []
card_list_not_flush.append(Card(2, 9))
card_list_not_flush.append(Card(3, 12))
card_list_not_flush.append(Card(2, 13))
card_list_not_flush.append(Card(2, 12))
card_list_not_flush.append(Card(3, 11))
card_list_not_flush.append(Card(0, 9))
card_list_not_flush.append(Card(2, 8))
assert hr1.getRank(ppo1, card_list_not_flush) != hr1.RANK_FLUSH

""" Straight test """
card_list_straight = []
card_list_straight.append(Card(2, 8))
card_list_straight.append(Card(3, 9))
card_list_straight.append(Card(2, 10))
card_list_straight.append(Card(1, 11))
card_list_straight.append(Card(3, 12))
card_list_straight.append(Card(2, 5))
card_list_straight.append(Card(2, 14))
assert hr1.getRank(ppo1, card_list_straight) == hr1.RANK_STRAIGHT

""" Not straight test """
card_list_not_straight = []
card_list_not_straight.append(Card(2, 9))
card_list_not_straight.append(Card(3, 10))
card_list_not_straight.append(Card(2, 11))
card_list_not_straight.append(Card(1, 12))
card_list_not_straight.append(Card(3, 7))
card_list_not_straight.append(Card(0, 11))
card_list_not_straight.append(Card(2, 14))
assert hr1.getRank(ppo1, card_list_not_straight) != hr1.RANK_STRAIGHT

""" Three of a kind test """
card_list_three_of_a_kind = []
card_list_three_of_a_kind.append(Card(2, 8))
card_list_three_of_a_kind.append(Card(3, 9))
card_list_three_of_a_kind.append(Card(2, 14))
card_list_three_of_a_kind.append(Card(1, 14))
card_list_three_of_a_kind.append(Card(3, 14))
card_list_three_of_a_kind.append(Card(2, 5))
card_list_three_of_a_kind.append(Card(2, 12))
assert hr1.getRank(ppo1, card_list_three_of_a_kind) == hr1.RANK_THREE_OF_A_KIND

""" Not three of a kind test """
card_list_not_three_of_a_kind = []
card_list_not_three_of_a_kind.append(Card(2, 9))
card_list_not_three_of_a_kind.append(Card(3, 9))
card_list_not_three_of_a_kind.append(Card(2, 11))
card_list_not_three_of_a_kind.append(Card(1, 11))
card_list_not_three_of_a_kind.append(Card(3, 7))
card_list_not_three_of_a_kind.append(Card(0, 7))
card_list_not_three_of_a_kind.append(Card(2, 12))
assert hr1.getRank(ppo1, card_list_not_three_of_a_kind) != hr1.RANK_THREE_OF_A_KIND

""" Two pair test """
card_list_two_pair = []
card_list_two_pair.append(Card(2, 8))
card_list_two_pair.append(Card(3, 9))
card_list_two_pair.append(Card(2, 14))
card_list_two_pair.append(Card(1, 14))
card_list_two_pair.append(Card(3, 8))
card_list_two_pair.append(Card(2, 5))
card_list_two_pair.append(Card(2, 12))
assert hr1.getRank(ppo1, card_list_two_pair) == hr1.RANK_TWO_PAIR

""" Not two pair test """
card_list_not_two_pair = []
card_list_not_two_pair.append(Card(2, 9))
card_list_not_two_pair.append(Card(3, 10))
card_list_not_two_pair.append(Card(2, 11))
card_list_not_two_pair.append(Card(1, 11))
card_list_not_two_pair.append(Card(3, 6))
card_list_not_two_pair.append(Card(0, 8))
card_list_not_two_pair.append(Card(2, 13))
assert hr1.getRank(ppo1, card_list_not_two_pair) != hr1.RANK_TWO_PAIR

""" Pair test """
card_list_pair = []
card_list_pair.append(Card(2, 14))
card_list_pair.append(Card(3, 9))
card_list_pair.append(Card(2, 2))
card_list_pair.append(Card(1, 2))
card_list_pair.append(Card(3, 8))
card_list_pair.append(Card(2, 5))
card_list_pair.append(Card(2, 12))
assert hr1.getRank(ppo1, card_list_pair) == hr1.RANK_PAIR

""" Not pair test """
card_list_not_pair = []
card_list_not_pair.append(Card(2, 9))
card_list_not_pair.append(Card(3, 10))
card_list_not_pair.append(Card(2, 11))
card_list_not_pair.append(Card(1, 12))
card_list_not_pair.append(Card(3, 6))
card_list_not_pair.append(Card(0, 7))
card_list_not_pair.append(Card(2, 14))
assert hr1.getRank(ppo1, card_list_not_pair) != hr1.RANK_PAIR

""" Extra test 1 """
card_list_extra_1 = []
card_list_extra_1.append(Card(2, 7))
card_list_extra_1.append(Card(0, 5))
card_list_extra_1.append(Card(3, 3))
card_list_extra_1.append(Card(0, 14))
card_list_extra_1.append(Card(1, 12))
card_list_extra_1.append(Card(0, 2))
card_list_extra_1.append(Card(1, 2))
assert hr1.getRank(ppo1, card_list_extra_1) == hr1.RANK_PAIR

""" Extra test 2 """
card_list_extra_2 = []
card_list_extra_2.append(Card(3, 2))
card_list_extra_2.append(Card(3, 5))
card_list_extra_2.append(Card(3, 3))
card_list_extra_2.append(Card(0, 14))
card_list_extra_2.append(Card(1, 12))
card_list_extra_2.append(Card(0, 2))
card_list_extra_2.append(Card(1, 2))
assert hr1.getRank(ppo1, card_list_extra_2) == hr1.RANK_THREE_OF_A_KIND

