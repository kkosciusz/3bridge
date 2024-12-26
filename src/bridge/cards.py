"""Basic types for bridge card game."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class Suit(Enum):
    """Suit of the bridge playing card."""

    CLUB = 0
    DIAMOND = 1
    HEART = 2
    SPADE = 3

    def __repr__(self):
        return f'{self.__class__.__name__}.{self._name_}'

    def __lt__(self, other):
        if self.__class__ == other.__class__:
            return self.value < other.value
        raise NotImplementedError

    @classmethod
    def __strings(cls):
        return ('C', 'D', 'H', 'S')

    def as_text(self) -> str:
        """Return text representation of the Suit."""
        return Suit.__strings()[self.value]

    @classmethod
    def from_text(cls, text: str) -> Suit:
        """Create a Suit from the text representation."""
        return cls(cls.__strings().index(text))


class Rank(Enum):
    """Rank of the bridge playing card."""

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

    def __repr__(self):
        return f'{self.__class__.__name__}.{self._name_}'

    @classmethod
    def __strings(cls):
        return ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')

    def __lt__(self, other: Rank):
        if self.__class__ == other.__class__:
            return self.value < other.value
        raise NotImplementedError

    def as_text(self) -> str:
        """Return text representation of the Rank."""
        return Rank.__strings()[self.value]

    @classmethod
    def from_text(cls, text: str) -> Rank:
        """Create a Rank from text representation."""
        return cls(cls.__strings().index(text))


@dataclass(eq=True, frozen=True)
class Card:
    """One bridge playing card."""

    suit: Suit
    rank: Rank

    def __repr__(self):
        return f'Card({self.suit}, {self.rank})'

    @classmethod
    def from_text(cls, text: str):
        """Create a card from text representation."""
        return cls(Suit.from_text(text[0]), Rank.from_text(text[1:]))

    def as_text(self) -> str:
        """Return text representation of the Card."""
        return self.suit.as_text() + self.rank.as_text()

    def points(self) -> int:
        """Calculate point value of the Card."""
        points = {
            Rank.ACE: 4,
            Rank.KING: 3,
            Rank.QUEEN: 2,
            Rank.JACK: 1,
        }
        return points.get(self.rank, 0)


class Hand:
    """Hand of bridge cards."""

    _cards: set[Card]

    def __repr__(self) -> str:
        return f'Hand.from_text({self.as_text()!r})'

    def __init__(self, cards=None):
        self._cards = set(cards) if cards is not None else set()

    def __len__(self):
        return len(self._cards)

    def __iter__(self):
        return iter(self._cards)

    def add(self, card: Card) -> None:
        """Add a Card to Hand. Throws if Card is already in Hand."""
        if card in self._cards:
            msg = f'{card!r} already in hand'
            raise ValueError(msg)
        self._cards.add(card)

    def points(self) -> int:
        """Calculate point value of the cards in Hand."""
        return sum(card.points() for card in self._cards)

    def as_text(self) -> str:
        """Return text representation of the Hand."""
        suits = sorted(Suit, reverse=True)
        suit_ranks = {suit: [] for suit in suits}
        for card in self._cards:
            suit_ranks[card.suit].append(card.rank)

        def stringize(ranks):
            return "".join(map(Rank.as_text, sorted(ranks, reverse=True)))

        return ".".join(stringize(suit_ranks[suit]) for suit in suits)

    @classmethod
    def from_text(cls: type[Hand], text: str) -> Hand:
        """Create a bridge Hand from text representation."""
        suits = [Suit.SPADE, Suit.HEART, Suit.DIAMOND, Suit.CLUB]
        rank_re = re.compile(r"[AKQJ98765432]|10")
        rank_texts = [rank_re.findall(cards) for cards in text.split('.')]

        if len(rank_texts) != len(suits):
            msg = f"expecting exactly {len(suits)} suits"
            raise ValueError(msg)

        rebuilt = ".".join("".join(list(rank_text)) for rank_text in rank_texts)
        if rebuilt != text:
            msg = "unknown card rank"
            raise ValueError(msg)

        hand = cls()
        for suit, ranks in zip(suits, rank_texts):
            for rank in ranks:
                card = Card(suit, Rank.from_text(rank))
                hand.add(card)
        return hand


ALL_CARDS = tuple(Card(suit, rank) for rank in Rank for suit in Suit)
