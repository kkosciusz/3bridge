"""Operations on Hands and Cards."""

from enum import Enum
from dataclasses import dataclass


class Suit(Enum):
    SPADE = 1
    HEART = 2
    DIAMOND = 3
    CLUB = 4


@dataclass(eq=True, frozen=True, slots=True)
class Card:
    suit: Suit
    rank: str


class Hand:
    """Represent a set of cards for one player."""
    _cards: set[Card]

    def __init__(self):
        self._cards = set()

    def __len__(self):
        return len(self._cards)

    def __iter__(self):
        return iter(self._cards)

    def add(self, card: Card):
        if card in self._cards:
            raise ValueError
        self._cards.add(card)
