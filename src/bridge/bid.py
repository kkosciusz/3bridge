"""Bids and operations in a bridge card game."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Trump(Enum):
    """Trump of a Bid in a bridge game."""

    CLUB = 0
    DIAMOND = 1
    HEART = 2
    SPADE = 3
    NOTRUMP = 4

    @classmethod
    def __strings(cls):
        return ('C', 'D', 'H', 'S', 'NT')

    def as_text(self) -> str:
        return Trump.__strings()[self.value]


@dataclass(eq=True, frozen=True)
class Bid:
    """Contract Bid in a bridge game."""

    count: int
    trump: Trump

    def as_text(self) -> str:
        return f"{self.count}{self.trump.as_text()}"
