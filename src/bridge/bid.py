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


@dataclass(eq=True, frozen=True)
class Bid:
    trump: Trump
    count: int
