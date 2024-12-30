"""Common bidding system for bridge card game."""

from __future__ import annotations

from bridge.bid import Bid, Trump
from bridge.cards import Suit
from bridge.conditions import (
    cards,
    cards_min,
    cards_range,
    points_min,
    points_range,
)
from bridge.rules import Rule

open_1_clubs_natural = Rule(
    Bid(1, Trump.CLUB),
    require=[points_range(12, 17), cards_min(5, Suit.CLUB)],
    note="natural",
)
open_1_clubs_balanced = Rule(
    Bid(1, Trump.CLUB),
    require=[points_range(12, 17)],
    exclude=[
        cards_min(5, Suit.SPADE),
        cards_min(5, Suit.HEART),
        cards_min(5, Suit.DIAMOND),
        cards_min(5, Suit.CLUB),
    ],
    note="balanced",
)
open_1_clubs_strong = Rule(
    Bid(1, Trump.CLUB), require=[points_range(18, 22)], note="strong"
)
open_1_diamonds = Rule(
    Bid(1, Trump.DIAMOND), require=[points_range(12, 17), cards_min(5, Suit.DIAMOND)]
)
open_1_hearts = Rule(
    Bid(1, Trump.HEART), require=[points_range(12, 17), cards_min(5, Suit.HEART)]
)
open_1_spades = Rule(
    Bid(1, Trump.SPADE), require=[points_range(12, 17), cards_min(5, Suit.SPADE)]
)
open_1_notrump = Rule(
    Bid(1, Trump.NOTRUMP),
    require=[
        points_range(15, 17),
        cards_range(3, 4, Suit.HEART),
        cards_range(3, 4, Suit.SPADE),
        cards_range(3, 5, Suit.CLUB),
        cards_range(3, 5, Suit.DIAMOND),
    ],
)
open_2_clubs = Rule(Bid(2, Trump.CLUB), require=[points_min(23)])
open_2_diamonds = Rule(
    Bid(2, Trump.DIAMOND),
    require=[cards(6, Suit.DIAMOND), points_range(7, 11)],
    exclude=[cards_min(4, Suit.HEART), cards_min(4, Suit.SPADE)],
)
open_2_hearts = Rule(
    Bid(2, Trump.HEART),
    require=[cards(6, Suit.HEART), points_range(7, 11)],
    exclude=[cards_min(4, Suit.SPADE)],
)
open_2_spades = Rule(
    Bid(2, Trump.SPADE),
    require=[cards(6, Suit.SPADE), points_range(7, 11)],
    exclude=[cards_min(4, Suit.HEART)],
)
open_2_notrump = Rule(
    Bid(2, Trump.NOTRUMP),
    require=[
        points_range(23, 24),
        cards_range(2, 4, Suit.SPADE),
        cards_range(2, 4, Suit.HEART),
        cards_range(2, 4, Suit.DIAMOND),
        cards_range(2, 4, Suit.CLUB),
    ],
)
open_3_clubs = Rule(
    Bid(3, Trump.CLUB), require=[points_range(6, 10), cards_min(7, Suit.CLUB)]
)
open_3_diamonds = Rule(
    Bid(3, Trump.DIAMOND), require=[points_range(6, 10), cards_min(7, Suit.DIAMOND)]
)
open_3_hearts = Rule(
    Bid(3, Trump.HEART), require=[points_range(6, 10), cards_min(7, Suit.HEART)]
)
open_3_spades = Rule(
    Bid(3, Trump.SPADE), require=[points_range(6, 10), cards_min(7, Suit.SPADE)]
)

all_openings = [
    open_1_clubs_balanced,
    open_1_clubs_natural,
    open_1_clubs_strong,
    open_1_diamonds,
    open_1_hearts,
    open_1_spades,
    open_1_notrump,
    open_2_clubs,
    open_2_diamonds,
    open_2_hearts,
    open_2_spades,
    open_2_notrump,
    open_3_clubs,
    open_3_diamonds,
    open_3_hearts,
    open_3_spades,
]
