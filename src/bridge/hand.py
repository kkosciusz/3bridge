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

    @classmethod
    def from_text(cls, text):
        suits = {
            'S': Suit.SPADE,
            'H': Suit.HEART,
            'D': Suit.DIAMOND,
            'C': Suit.CLUB,
        }
        return cls(suits[text[0]], text[1])

    def as_text(self):
        suits = {
           Suit.SPADE: 'S',
           Suit.HEART: 'H',
           Suit.DIAMOND: 'D',
           Suit.CLUB: 'C',
        }
        return suits[self.suit] + self.rank


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
