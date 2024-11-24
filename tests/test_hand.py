import pytest

from bridge.hand import Card, Hand, Suit


def test_empty_hand_has_len_0():
    hand = Hand()
    assert len(hand) == 0


def test_after_adding_card_to_empty_hand_card_is_in_hand():
    hand = Hand()
    card = Card(Suit.SPADE, 'A')
    hand.add(card)
    assert card in hand


def test_adding_a_card_to_a_hand_twice_throws():
    hand = Hand()
    card = Card(Suit.SPADE, 'A')
    hand.add(card)
    with pytest.raises(ValueError):
        hand.add(card)
