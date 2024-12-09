import pytest
from bridge.conditions import (
    cards,
    cards_max,
    cards_min,
    cards_range,
    pc,
    pc_max,
    pc_min,
    pc_range,
)
from bridge.hand import Suit


@pytest.mark.parametrize("number", range(1, 24, 2))
def test_description_of_exact_points_for_whole_hand(number):
    condition = pc(number)
    assert condition.describe() == f"{number} PC"


@pytest.mark.parametrize("number", range(1, 24, 2))
def test_description_of_minimum_points_for_whole_hand(number):
    condition = pc_min(number)
    assert condition.describe() == f"od {number} PC"


@pytest.mark.parametrize("number", range(1, 24, 2))
def test_description_of_maximum_points_for_whole_hand(number):
    condition = pc_max(number)
    assert condition.describe() == f"do {number} PC"


@pytest.mark.parametrize("start", [1, 5, 8])
@pytest.mark.parametrize("add", [1, 2, 5])
def test_description_of_points_range_for_whole_hand(start, add):
    condition = pc_range(start, start + add)
    assert condition.describe() == f"{start}-{start+add} PC"


@pytest.mark.parametrize(
    ("suit", "text"),
    [
        (Suit.CLUB, "trefli"),
        (Suit.DIAMOND, "kar"),
        (Suit.HEART, "kierów"),
        (Suit.SPADE, "pików"),
    ],
)
@pytest.mark.parametrize("count", [2, 4, 5])
def test_description_of_exact_suit_card_count(suit, text, count):
    condition = cards(count, suit=suit)
    assert condition.describe() == f"{count} {text}"


@pytest.mark.parametrize(
    ("suit", "text"),
    [
        (Suit.CLUB, "trefli"),
        (Suit.DIAMOND, "kar"),
        (Suit.HEART, "kierów"),
        (Suit.SPADE, "pików"),
    ],
)
@pytest.mark.parametrize("count", [2, 4, 5])
def test_description_of_min_suit_card_count(suit, text, count):
    condition = cards_min(count, suit=suit)
    assert condition.describe() == f"od {count} {text}"


@pytest.mark.parametrize(
    ("suit", "text"),
    [
        (Suit.CLUB, "trefli"),
        (Suit.DIAMOND, "kar"),
        (Suit.HEART, "kierów"),
        (Suit.SPADE, "pików"),
    ],
)
@pytest.mark.parametrize("count", [2, 4, 5])
def test_description_of_max_suit_card_count(suit, text, count):
    condition = cards_max(count, suit=suit)
    assert condition.describe() == f"do {count} {text}"


@pytest.mark.parametrize(
    ("suit", "text"),
    [
        (Suit.CLUB, "trefli"),
        (Suit.DIAMOND, "kar"),
        (Suit.HEART, "kierów"),
        (Suit.SPADE, "pików"),
    ],
)
@pytest.mark.parametrize("start", [1, 5, 8])
@pytest.mark.parametrize("add", [1, 2, 5])
def test_description_of_min_max_suit_card_count(suit, text, start, add):
    condition = cards_range(start, start + add, suit=suit)
    assert condition.describe() == f"od {start} do {start+add} {text}"
