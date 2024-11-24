"""Operations on Hands and Cards."""


class Card:
    pass


class Hand:
    """Represent a set of cards for one player."""
    def __init__(self):
        self._cards = 0

    def __len__(self):
        return self._cards

    def add(self, card: Card):
        self._cards += 1
