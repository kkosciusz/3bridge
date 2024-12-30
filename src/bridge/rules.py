"""Bidding rules for a bridge card game."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bridge.bid import Bid
    from bridge.conditions import Condition


@dataclass
class Rule:
    bid: Bid
    require: list[Condition] = field(default_factory=list)
    exclude: list[Condition] = field(default_factory=list)
    note: str | None = None

    def describe(self):
        result = self.bid.as_text()
        require_text = ", ".join(c.describe() for c in self.require)
        exclude_text = ", ".join(c.describe() for c in self.exclude)
        if require_text or exclude_text:
            result += ":"
        if require_text:
            result += f" {require_text}"
        if exclude_text:
            result += f" wyklucza {exclude_text}"
        return result

    def match(self, hand):
        """Match the rule against a given hand."""
        required_match = all(cond.evaluate(hand) for cond in self.require)
        excluded_match = all(not cond.evaluate(hand) for cond in self.exclude)
        return required_match and excluded_match

    def as_text(self) -> str:
        text = self.bid.as_text()
        if self.note:
            text += f" ({self.note})"
        return text
