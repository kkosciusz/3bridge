import pytest
from bridge.bidding import (
    open_1_clubs_balanced,
    open_1_clubs_natural,
    open_1_clubs_strong,
    open_1_diamonds,
    open_1_hearts,
    open_1_notrump,
    open_1_spades,
)
from bridge.cards import Hand


@pytest.mark.parametrize(
    ('rule', 'hand_text', 'expected'),
    [
        (open_1_clubs_natural, '87.AJ10.QJ3.KQ1075', True),
        (open_1_clubs_natural, '87.AJ1087.QJ3.KQ10', False),  # not enough clubs
        (open_1_clubs_natural, '87.987.QJ3.KQ1043', False),  # not enough points
        (open_1_clubs_natural, 'AK.AK7.QJ3.KQ1043', False),  # too many points
        (open_1_clubs_balanced, 'KQJ8.KQJ8.9876.J', True),
        (open_1_clubs_balanced, 'KQ87.QJ87.Q876.J', False),  # not enough points
        (open_1_clubs_balanced, 'AKQ8.AKQ8.9876.J', False),  # too many points
        (open_1_clubs_balanced, 'KQJ87.KQJ8.986.J', False),  # too many spades
        (open_1_clubs_balanced, 'KQJ8.KQJ87.986.J', False),  # too many hearts
        (open_1_clubs_balanced, 'KQJ.KQJ8.109876.J', False),  # too many diamonds
        (open_1_clubs_balanced, 'KQJ.KQJ8.J.109876', False),  # too many clubs
        (open_1_clubs_strong, 'AKQJ.AKQJ.9876.J', True),
        (open_1_clubs_strong, 'AKQJ.AKQJ.9876.K', False),  # too many points
        (open_1_clubs_strong, 'AKQ8.AKJ9.9876.8', False),  # not enough points
        (open_1_diamonds, '87.AJ10.KQ1075.QJ3', True),
        (open_1_diamonds, '87.AJ1087.KQ10.QJ3', False),  # not enough diamonds
        (open_1_diamonds, 'K7.987.KQ1043.QJ3', False),  # not enough points
        (open_1_diamonds, 'AK.AK7.KQ1043.873', False),  # too many points
        (open_1_hearts, '87.KQ1075.AJ10.QJ3', True),
        (open_1_hearts, '87.KQ108.AJ87.QJ3', False),  # not enough hearts
        (open_1_hearts, 'J7.KQ1043.A87.J83', False),  # not enough points
        (open_1_hearts, 'KQ.KQ1043.A87.KJ3', False),  # too many points
        (open_1_spades, 'KQ1075.87.AJ10.QJ3', True),
        (open_1_spades, 'KQ108.A87.J87.QJ3', False),  # not enough spades
        (open_1_spades, 'KQ1043.J7.A87.J83', False),  # not enough points
        (open_1_spades, 'KQ1043.KQ.A87.KJ3', False),  # too many points
        (open_1_notrump, 'KQ87.KQ8.KJ7.Q97', True),
        (open_1_notrump, 'KQ87.KQ8.Q87.Q97', False),  # not enough points
        (open_1_notrump, 'KQ87.KQ8.AQ7.Q97', False),  # not too many points
        (open_1_notrump, 'KQ8.KQ876.KJ6.Q97', False),  # too many hearts
        (open_1_notrump, 'KQ876.KQ8.KJ6.Q97', False),  # too many spades
        (open_1_notrump, 'KQ87.KQ87.KJ76.Q9', False),  # not enough clubs
        (open_1_notrump, 'KQ87.KQ87.Q9.KJ76', False),  # not enough diamonds
        (open_1_notrump, 'KQ87.Q9.KQ87.KJ76', False),  # not enough hearts
        (open_1_notrump, 'Q9.KQ87.KQ87.KJ76', False),  # not enough spades
    ],
)
def test_opening_1_examples_should_match_hand_as_expected(rule, hand_text, expected):
    hand = Hand.from_text(hand_text)
    assert rule.match(hand) is expected
