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
