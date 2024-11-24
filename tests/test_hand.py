from bridge.hand import Hand


def test_empty_hand():
    hand = Hand()
    assert len(hand) == 0
