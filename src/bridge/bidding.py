"""Common bidding system for bridge card game."""

from __future__ import annotations

from bridge.bid import Bid, Trump
from bridge.cards import Suit
from bridge.conditions import (
    cards_min,
    cards_range,
    points_range,
)
from bridge.rules import Rule

open_1_clubs_natural = Rule(
    Bid(Trump.CLUB, 1), require=[points_range(12, 17), cards_min(5, Suit.CLUB)]
)
open_1_clubs_balanced = Rule(
    Bid(Trump.CLUB, 1),
    require=[points_range(12, 17)],
    exclude=[
        cards_min(5, Suit.SPADE),
        cards_min(5, Suit.HEART),
        cards_min(5, Suit.DIAMOND),
        cards_min(5, Suit.CLUB),
    ],
)
open_1_clubs_strong = Rule(Bid(Trump.CLUB, 1), require=[points_range(18, 22)])
open_1_diamonds = Rule(
    Bid(Trump.DIAMOND, 1), require=[points_range(12, 17), cards_min(5, Suit.DIAMOND)]
)
open_1_hearts = Rule(
    Bid(Trump.HEART, 1), require=[points_range(12, 17), cards_min(5, Suit.HEART)]
)
open_1_spades = Rule(
    Bid(Trump.SPADE, 1), require=[points_range(12, 17), cards_min(5, Suit.SPADE)]
)
open_1_notrump = Rule(
    Bid(Trump.NOTRUMP, 1),
    require=[
        points_range(15, 17),
        cards_range(3, 4, Suit.HEART),
        cards_range(3, 4, Suit.SPADE),
        cards_range(3, 5, Suit.CLUB),
        cards_range(3, 5, Suit.DIAMOND),
    ],
)
