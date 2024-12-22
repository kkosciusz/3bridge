import pytest
from bridge.bid import Bid, Trump
from bridge.cards import Hand, Suit
from bridge.conditions import (
    cards_min,
    points,
    points_min,
    points_range,
)
from bridge.rules import Rule

# CLUB = '♣'
# DIAMOND = '♦'
# SPADE = '♠'
# HEART = '♥'
CLUB = 'C'
DIAMOND = 'D'
SPADE = 'S'
HEART = 'H'
NOTRUMP = 'NT'


@pytest.mark.parametrize(
    ("trump", "symbol"),
    [
        (Trump.CLUB, CLUB),
        (Trump.DIAMOND, DIAMOND),
        (Trump.SPADE, SPADE),
        (Trump.HEART, HEART),
        (Trump.NOTRUMP, NOTRUMP),
    ],
)
@pytest.mark.parametrize("count", [1, 3, 5])
def test_can_describe_rule_without_conditions(trump, symbol, count):
    rule = Rule(bid=Bid(trump, count))
    assert rule.describe() == f"{count}{symbol}"


def test_can_describe_rule_with_one_required_pc_condition():
    bid = Bid(Trump.CLUB, 1)
    condition = points_min(10)
    rule = Rule(bid=bid, require=[condition])
    assert rule.describe() == f"1{CLUB}: {condition.describe()}"


def test_can_describe_rule_with_one_excluded_pc_condition():
    bid = Bid(Trump.CLUB, 1)
    condition = points_min(10)
    rule = Rule(bid=bid, exclude=[condition])
    assert rule.describe() == f"1{CLUB}: wyklucza {condition.describe()}"


def test_can_describe_rule_with_one_required_and_one_excluded_pc_condition():
    bid = Bid(Trump.CLUB, 1)
    require = points_min(10)
    exclude = points(20)
    rule = Rule(bid=bid, require=[require], exclude=[exclude])
    assert (
        rule.describe()
        == f"1{CLUB}: {require.describe()} wyklucza {exclude.describe()}"
    )


def test_can_describe_complex_1nt_rule_with_requires_and_excludes_conditions():
    bid = Bid(Trump.NOTRUMP, 1)
    require = [
        points_range(15, 17),
        cards_min(2, Suit.CLUB),
        cards_min(2, Suit.DIAMOND),
        cards_min(2, Suit.HEART),
        cards_min(2, Suit.SPADE),
    ]
    exclude = [cards_min(5, Suit.HEART), cards_min(5, Suit.SPADE)]
    rule = Rule(bid=bid, require=require, exclude=exclude)
    expected = (
        f"1{NOTRUMP}: 15-17 PC, od 2 trefli, od 2 kar, "
        "od 2 kierów, od 2 pików wyklucza od 5 kierów, od 5 pików"
    )
    assert rule.describe() == expected


def test_rule_matches_only_if_all_required_conditions_match():
    bid = Bid(Trump.HEART, 1)
    rule = Rule(bid, require=[points_range(12, 15), cards_min(5, Suit.HEART)])
    hand_5h_15pc = Hand.from_text('987.AKQJ9.654.AJ')
    assert rule.match(hand_5h_15pc) is True
    hand_4h_15pc = Hand.from_text('987.AKQJ.9654.AJ')
    assert rule.match(hand_4h_15pc) is False
    hand_5h_10pc = Hand.from_text('987.AKQJ9.9654.87')
    assert rule.match(hand_5h_10pc) is False
    hand_4h_10pc = Hand.from_text('987.AKQJ.9654.87')
    assert rule.match(hand_4h_10pc) is False


def test_rule_matches_only_if_no_excluded_condition_matches():
    bid = Bid(Trump.HEART, 1)
    rule = Rule(bid, exclude=[points_min(15), cards_min(4, Suit.CLUB)])
    hand_5c_12pc = Hand.from_text('Q87.98.654.AKQJ9')
    assert rule.match(hand_5c_12pc) is False
    hand_3c_12pc = Hand.from_text('Q87.98.J9654.AKQ')
    assert rule.match(hand_3c_12pc) is True
    hand_3c_16pc = Hand.from_text('Q87.A8.J9654.AKQ')
    assert rule.match(hand_3c_16pc) is False
    hand_5c_16pc = Hand.from_text('Q87.A8.J96.AKQ54')
    assert rule.match(hand_5c_16pc) is False
