"""Operations on Bids."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Trump(Enum):
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
    trump: Trump
    count: int

    def as_text(self) -> str:
        return f"{self.count}{self.trump.as_text()}"
