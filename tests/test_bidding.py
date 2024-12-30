import pytest
from bridge.bidding import (
    open_1_clubs_balanced,
    open_1_clubs_natural,
    open_1_clubs_strong,
    open_1_diamonds,
    open_1_hearts,
    open_1_notrump,
    open_1_spades,
    open_2_clubs,
    open_2_diamonds,
    open_2_hearts,
    open_2_notrump,
    open_2_spades,
    open_3_clubs,
    open_3_diamonds,
    open_3_hearts,
    open_3_spades,
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
        (open_2_clubs, 'AKQ.AKQ.AKQ.AQK3', True),
        (open_2_clubs, 'AJ10.AJ10.AJ10.AQ109', False),  # not enough points
        (open_2_diamonds, '987.753.AK9876.9', True),
        (open_2_diamonds, 'J87.Q53.AK9876.J', True),
        (open_2_diamonds, '987.753.AK987.96', False),  # not enough diamonds
        (open_2_diamonds, '987.753.AQ9876.9', False),  # not enough points
        (open_2_diamonds, '987.Q53.AKQJ76.9', False),  # too many points
        (open_2_diamonds, 'J8.Q536.AK9876.J', False),  # too many hearts
        (open_2_diamonds, 'Q536.J8.AK9876.J', False),  # too many spades
        (open_2_hearts, 'J87.AK9876.Q53.J', True),
        (open_2_hearts, 'J87.A109876.Q53.9', True),
        (open_2_hearts, 'J87.AK987.Q53.J6', False),  # not enough hearts
        (open_2_hearts, 'J87.AK98753.Q.J6', False),  # too many hearts
        (open_2_hearts, 'J87.AJ9876.953.8', False),  # not enough points
        (open_2_hearts, 'J875.AQJ876.A3.8', False),  # too many points
        (open_2_hearts, 'J875.AK9876.Q3.J', False),  # too many spades
        (open_2_hearts, 'QJ875.AK9876.3.J', False),  # too many spades
        (open_2_spades, 'AK9876.J87.Q53.J', True),
        (open_2_spades, 'A109876.J87.Q53.9', True),
        (open_2_spades, 'J87.AK987.Q53.J6', False),  # not enough spades
        (open_2_spades, 'AK98753.J87.Q.J6', False),  # too many spades
        (open_2_spades, 'AJ9876.J87.953.8', False),  # not enough points
        (open_2_spades, 'AQJ876.J875.A3.8', False),  # too many points
        (open_2_spades, 'AK9876.J875.Q3.J', False),  # too many hearts
        (open_2_spades, 'AK9876.QJ875.3.J', False),  # too many hearts
        (open_2_notrump, 'AK76.AK9.AK8.Q32', True),
        (open_2_notrump, 'AK76.AK9.AK8.J32', False),  # not enough points
        (open_2_notrump, 'AK76.AK9.AK8.A32', False),  # too many points
        (open_2_notrump, 'AK762.AK9.AK8.Q3', False),  # too many spades
        (open_2_notrump, 'AK7.AK962.AK8.Q3', False),  # too many hearts
        (open_2_notrump, 'AK7.AK9.AK862.Q3', False),  # too many diamonds
        (open_2_notrump, 'AK7.AK.AK8.Q9632', False),  # too many clubs
        (open_2_notrump, 'K.AK76.AK98.AQ32', False),  # not enough spades
        (open_2_notrump, 'AK76.K.AK98.AQ32', False),  # not enough hearts
        (open_2_notrump, 'AK76.AK98.K.AQ32', False),  # not enough diamonds
        (open_2_notrump, 'AK76.AK98.AQ32.K', False),  # not enough clubs
        (open_3_clubs, '98.6.J74.AJ96532', True),
        (open_3_clubs, '98.652.72.AJ96543', False),  # not enough points
        (open_3_clubs, '98.J52.72.AKQJ965', False),  # too many points
        (open_3_clubs, '98.652.J7.AJ9543', False),  # not enough clubs
        (open_3_diamonds, '98.6.AJ96532.J74', True),
        (open_3_diamonds, '98.652.AJ96543.72', False),  # not enough points
        (open_3_diamonds, '98.J52.AKQJ965.72', False),  # too many points
        (open_3_diamonds, '98.652.AJ9543.J7', False),  # not enough diamonds
        (open_3_hearts, '98.AJ96532.6.J74', True),
        (open_3_hearts, '98.AJ96543.652.72', False),  # not enough points
        (open_3_hearts, '98.AKQJ965.J52.72', False),  # too many points
        (open_3_hearts, '98.AJ9543.652.J7', False),  # not enough hearts
        (open_3_spades, 'AJ96532.98.6.J74', True),
        (open_3_spades, 'AJ96543.98.652.72', False),  # not enough points
        (open_3_spades, 'AKQJ965.98.J52.72', False),  # too many points
        (open_3_spades, 'AJ9543.98.652.J7', False),  # not enough spades
    ],
)
def test_opening_1_examples_should_match_hand_as_expected(rule, hand_text, expected):
    hand = Hand.from_text(hand_text)
    assert rule.match(hand) is expected
