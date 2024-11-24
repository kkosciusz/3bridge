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


def test_comparing_cards_for_equality_is_supported():
    card1 = Card(Suit.SPADE, 'A')
    card2 = Card(Suit.HEART, 'A')
    card3 = Card(Suit.HEART, 'K')
    card4 = Card(Suit.SPADE, 'A')

    assert card1 == card4
    assert card1 != card2
    assert card2 != card3
    assert card3 != card4


def test_can_parse_card_from_text():
    card = Card.from_text('SA')
    assert card == Card(Suit.SPADE, 'A')


def test_can_output_card_as_text():
    card = Card(Suit.SPADE, 'A')
    assert card.as_text() == 'SA'
