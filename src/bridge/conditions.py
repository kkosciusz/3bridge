from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from bridge.hand import Hand, Suit


def pc(count: int) -> Condition:
    return Condition(Variable.PC, value_min=count, value_max=count)


def pc_min(count: int) -> Condition:
    return Condition(Variable.PC, value_min=count)


def pc_max(count: int) -> Condition:
    return Condition(Variable.PC, value_max=count)


def pc_range(count_min: int, count_max: int) -> Condition:
    return Condition(Variable.PC, value_min=count_min, value_max=count_max)


def cards(count: int, suit: Suit) -> Condition:
    return Condition(Variable.CARDS, value_min=count, value_max=count, suit=suit)


def cards_min(count: int, suit: Suit) -> Condition:
    return Condition(Variable.CARDS, value_min=count, suit=suit)


def cards_max(count: int, suit: Suit) -> Condition:
    return Condition(Variable.CARDS, value_max=count, suit=suit)


def cards_range(count_min: int, count_max: int, suit: Suit) -> Condition:
    return Condition(
        Variable.CARDS, value_min=count_min, value_max=count_max, suit=suit
    )


class Variable(Enum):
    PC = 1
    CARDS = 2


@dataclass
class Condition:
    variable: Variable
    value_min: int | None = None
    value_max: int | None = None
    suit: Suit | None = None

    def evaluate(self, hand: Hand) -> bool:
        return hand.hcl() == self.value_min

    def describe(self) -> str:
        if self.variable == Variable.PC:
            if self.value_max is not None and self.value_min is not None:
                if self.value_min == self.value_max:
                    return f"{self.value_max} PC"
                return f"{self.value_min}-{self.value_max} PC"
            if self.value_min is not None:
                return f"od {self.value_min} PC"
            if self.value_max is not None:
                return f"do {self.value_max} PC"
        elif self.variable == Variable.CARDS and self.suit is not None:
            suit_name = {
                Suit.CLUB: "trefli",
                Suit.DIAMOND: "kar",
                Suit.SPADE: "pików",
                Suit.HEART: "kierów",
            }[self.suit]
            if self.value_max is not None and self.value_min is not None:
                if self.value_min == self.value_max:
                    return f"{self.value_max} {suit_name}"
                return f"od {self.value_min} do {self.value_max} {suit_name}"
            if self.value_min is not None:
                return f"od {self.value_min} {suit_name}"
            if self.value_max is not None:
                return f"do {self.value_max} {suit_name}"
        return ""
