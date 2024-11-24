from bridge.hand import Card, Hand, Suit


def test_empty_hand_has_len_0():
    hand = Hand()
    assert len(hand) == 0


def test_can_add_card_to_hand():
    hand = Hand()
    ace_of_spades = Card(Suit.SPADE, 'A')
    hand.add(ace_of_spades)
    assert len(hand) == 1
    assert ace_of_spades in hand
