class Card(object):
    """ 
    " Represents a standard playing card.
    " 
    " Attributes:
    "     suit: integer 0-3
    "     rank: integer 2-14
    "
    """

    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = ["None", "None", "2", "3", "4", "5", "6", "7",
                  "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self, suit=2, rank=0):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        """ Returns a human-readable string representation."""
        return '%s of %s' % (Card.rank_names[self.rank],
                             Card.suit_names[self.suit])

    def __cmp__(self, other):
        """
        " Compares this card to other by rank only.
        "  
        " Returns 1 if this > other, -1 if this < other, 0 if equal
        "
        """
        return cmp(self.rank, other.rank)

