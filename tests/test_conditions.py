from __future__ import annotations

from typing import Callable, Sequence

import hypothesis.strategies as st
import pytest
from bridge.cards import ALL_CARDS, Card, Hand, Suit
from bridge.conditions import (
    Condition,
    cards,
    cards_max,
    cards_min,
    cards_range,
    points,
    points_max,
    points_min,
    points_range,
)
from hypothesis import given


@pytest.mark.parametrize("number", range(1, 24, 2))
def test_description_of_exact_points_for_whole_hand(number):
    condition = points(number)
    assert condition.describe() == f"{number} PC"


@pytest.mark.parametrize("number", range(1, 24, 2))
def test_description_of_minimum_points_for_whole_hand(number):
    condition = points_min(number)
    assert condition.describe() == f"od {number} PC"


@pytest.mark.parametrize("number", range(1, 24, 2))
def test_description_of_maximum_points_for_whole_hand(number):
    condition = points_max(number)
    assert condition.describe() == f"do {number} PC"


@pytest.mark.parametrize("start", [1, 5, 8])
@pytest.mark.parametrize("add", [1, 2, 5])
def test_description_of_points_range_for_whole_hand(start, add):
    condition = points_range(start, start + add)
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


def verify_hand_condition(
    hand: Hand, condition: Condition, expect: Callable[[Hand], bool]
) -> None:
    expected = expect(hand)
    assert condition.evaluate(hand) is expected


@st.composite
def n_card_hand(draw, n: int, cards: Sequence[Card] = ALL_CARDS) -> Hand:
    return draw(st.permutations(cards).map(lambda x: list(x)[:n]).map(Hand))


@given(hand=n_card_hand(13))
def test_point_conditions_evaluate_true_only_for_hands_with_correct_points(hand):
    verify_hand_condition(hand, points(10), lambda hand: hand.points() == 10)
    verify_hand_condition(hand, points_max(10), lambda hand: hand.points() <= 10)
    verify_hand_condition(hand, points_min(10), lambda hand: hand.points() >= 10)
    verify_hand_condition(
        hand, points_range(8, 12), lambda hand: 8 <= hand.points() <= 12
    )


@given(hand=n_card_hand(13), suit=st.sampled_from(Suit))
def test_one_suit_card_conditions_evaluate_correctly(hand, suit):
    verify_hand_condition(
        hand,
        cards(5, suit),
        lambda hand: 5 == sum(card.suit == suit for card in hand),
    )
    verify_hand_condition(
        hand,
        cards_min(5, suit),
        lambda hand: sum(card.suit == suit for card in hand) >= 5,
    )
    verify_hand_condition(
        hand,
        cards_max(5, suit),
        lambda hand: sum(card.suit == suit for card in hand) <= 5,
    )
    verify_hand_condition(
        hand,
        cards_range(4, 6, suit),
        lambda hand: 4 <= sum(card.suit == suit for card in hand) <= 6,
    )
