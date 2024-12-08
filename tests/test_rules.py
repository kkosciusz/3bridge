from bridge.rules import default_system
from bridge.bid import Bid, Trump


def test_first_opening_bid_is_one_clubs():
    opening_rules = default_system.get_opening()
    first_rule = opening_rules[0]
    assert first_rule.bid == Bid(Trump.CLUB, 1)


def test_can_describe_the_first_opening_bid():
    opening_rules = default_system.get_opening()
    first_rule = opening_rules[0]
    description = first_rule.describe()
    assert description.hcp_min == 12
    assert description.hcp_max == 17
    assert description.num_clubs_min == 5
