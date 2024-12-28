from __future__ import annotations

import random
import sys
from collections import Counter
from typing import TYPE_CHECKING, Iterable

from bridge.bidding import all_openings
from bridge.cards import ALL_CARDS, Hand
from prettytable import PrettyTable

if TYPE_CHECKING:
    from collections.abc import Generator

    from bridge.rules import Rule


def dealer(num_hands, min_points) -> Generator[Hand]:
    num_dealt = 0
    deck = list(ALL_CARDS)
    while num_dealt < num_hands:
        random.shuffle(deck)
        hand = Hand(deck[0:13])
        if hand.points() >= min_points:
            num_dealt += 1
            yield hand


def matching_openings(hand: Hand) -> Iterable[Rule]:
    return filter(lambda rule: rule.match(hand), all_openings)


class BidStats:
    def __init__(self):
        self.counter_ = Counter()

    def record(self, matches: list[Rule]):
        key = frozenset(rule.as_text() for rule in matches)
        self.counter_.update([key])

    def print(self, num_deals: int):
        table = PrettyTable()
        table.field_names = ["Matching bid(s)", "Count", "Percentage"]
        table.align["Matching bid(s)"] = 'l'
        table.align["Count"] = 'r'
        table.align["Percentage"] = 'r'
        for bids, count in self.counter_.items():
            text = " or ".join(sorted(bids)) or "no bid matches"
            table.add_row([text, count, f"{100*count/num_deals:.2f}"])
        print(table.get_string(sortby="Count", reversesort=True))


if __name__ == '__main__':
    args = sys.argv[1:]
    total_hands = int(args[0]) if len(args) > 0 else 1000
    min_points = int(args[1]) if len(args) > 1 else 12
    print(f"Generating {total_hands} hands, each with PC >= {min_points}.")
    stats = BidStats()
    for hand in dealer(total_hands, min_points):
        matches = list(matching_openings(hand))
        stats.record(matches)
    print("Bid distribution:")
    stats.print(total_hands)
