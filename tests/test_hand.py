from bridge.hand import Hand, Card


def test_empty_hand_has_len_0():
    hand = Hand()
    assert len(hand) == 0


def test_can_add_card_to_hand():
    hand = Hand()
    card = Card()
    hand.add(card)
    assert len(hand) == 1
