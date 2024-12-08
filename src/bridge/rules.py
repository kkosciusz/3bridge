from typing import Optional
from bridge.bid import Bid, Trump

from dataclasses import dataclass


class Rules:
    def get_opening(self):
        return [Rule()]


class Rule:
    def __init__(self):
        self.bid = Bid(Trump.CLUB, 1)

    def describe(self):
        return RuleDescription(hcp_min=12, hcp_max=17, num_clubs_min=5)


@dataclass(frozen=True)
class RuleDescription:
    hcp_min: int
    hcp_max: Optional[int] = None
    num_clubs_min: Optional[int] = None


default_system = Rules()
