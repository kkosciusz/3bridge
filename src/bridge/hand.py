"""Operations on Hands and Cards."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Suit(Enum):
    SPADE = 1
    HEART = 2
    DIAMOND = 3
    CLUB = 4

    def __repr__(self):
        return f'<{self.__class__.__name__}.{self._name_}>'


class Rank(Enum):
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    JACK = 9
    QUEEN = 10
    KING = 11
    ACE = 12

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            return cls._values().index(str)
        return super()._missing_(value)

    @classmethod
    def _values(cls):
        return ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')

    def __lt__(self, other):
        if self.__class__ == other.__class__:
            return self.value < other.value
        raise NotImplementedError

    def to_text(self):
        return Rank._values()[self.value]

    @classmethod
    def from_text(cls, text: str) -> Rank:
        return cls(cls._values().index(text))


@dataclass(eq=True, frozen=True)
class Card:
    suit: Suit
    rank: Rank

    @classmethod
    def from_text(cls, text):
        suits = {
            'S': Suit.SPADE,
            'H': Suit.HEART,
            'D': Suit.DIAMOND,
            'C': Suit.CLUB,
        }
        return cls(suits[text[0]], Rank.from_text(text[1:]))

    def as_text(self):
        suits = {
            Suit.SPADE: 'S',
            Suit.HEART: 'H',
            Suit.DIAMOND: 'D',
            Suit.CLUB: 'C',
        }
        return suits[self.suit] + self.rank.to_text()

    def hcl(self):
        hcls = {
            Rank.ACE: 4,
            Rank.KING: 3,
            Rank.QUEEN: 2,
            Rank.JACK: 1,
        }
        return hcls.get(self.rank, 0)


class Hand:
    """Represent a set of cards for one player."""

    _cards: set[Card]

    def __init__(self, cards=None):
        self._cards = set(cards) if cards is not None else set()

    def __len__(self):
        return len(self._cards)

    def __iter__(self):
        return iter(self._cards)

    def add(self, card: Card):
        if card in self._cards:
            msg = f'{card!r} already in hand'
            raise ValueError(msg)
        self._cards.add(card)

    def hcl(self):
        return sum(card.hcl() for card in self._cards)

    def as_text(self):
        spades, hearts, clubs, diamonds = [], [], [], []
        for card in self._cards:
            if card.suit == Suit.SPADE:
                spades += [card]
            if card.suit == Suit.HEART:
                hearts += [card]
            if card.suit == Suit.DIAMOND:
                diamonds += [card]
            if card.suit == Suit.CLUB:
                clubs += [card]

        def stringize(cards):
            ranks = sorted([card.rank for card in cards], reverse=True)
            return "".join(map(Rank.to_text, ranks))

        spades_str = stringize(spades)
        hearts_str = stringize(hearts)
        diamonds_str = stringize(diamonds)
        clubs_str = stringize(clubs)

        return f'{spades_str}.{hearts_str}.{diamonds_str}.{clubs_str}'
