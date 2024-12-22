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
    pc,
    pc_max,
    pc_min,
    pc_range,
)
from hypothesis import given


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


def verify_pc_condition(
    hand: Hand, condition: Condition, expect: Callable[[int], bool]
) -> None:
    points = hand.points()
    expected = expect(points)
    assert condition.evaluate(hand) is expected


@st.composite
def n_card_hand(draw, n: int, cards: Sequence[Card] = ALL_CARDS) -> Hand:
    return draw(st.permutations(cards).map(lambda x: list(x)[:n]).map(Hand))


@given(hand=n_card_hand(13))
def test_pc_conditions_evaluate_true_only_for_hands_with_correct_points(hand):
    verify_pc_condition(hand, pc(10), lambda pc: pc == 10)
    verify_pc_condition(hand, pc_max(10), lambda pc: pc <= 10)
    verify_pc_condition(hand, pc_min(10), lambda pc: pc >= 10)
    verify_pc_condition(hand, pc_range(8, 12), lambda pc: 8 <= pc <= 12)


def verify_cards_condition(
    hand: Hand, condition: Condition, expect: Callable[[Hand], bool]
) -> None:
    expected = expect(hand)
    assert condition.evaluate(hand) is expected


@given(hand=n_card_hand(13), suit=st.sampled_from(Suit))
def test_one_suit_card_conditions_evaluate_correctly(hand, suit):
    verify_cards_condition(
        hand,
        cards(5, suit),
        lambda hand: sum(card.suit == suit for card in hand) == 5,
    )
    verify_cards_condition(
        hand,
        cards_min(5, suit),
        lambda hand: sum(card.suit == suit for card in hand) >= 5,
    )
    verify_cards_condition(
        hand,
        cards_max(5, suit),
        lambda hand: sum(card.suit == suit for card in hand) <= 5,
    )
    verify_cards_condition(
        hand,
        cards_range(4, 6, suit),
        lambda hand: 4 <= sum(card.suit == suit for card in hand) <= 6,
    )
