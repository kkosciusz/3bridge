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
    with pytest.raises(ValueError, match="card already in hand"):
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


@pytest.mark.parametrize("rank_text", "A K Q J 10 9 8 7 6 5 4 3 2".split())
@pytest.mark.parametrize("suit_text", "S H D C".split())
def test_text_to_card_and_back_gives_same_text(suit_text, rank_text):
    card_text = suit_text + rank_text
    card = Card.from_text(card_text)
    assert card.as_text() == card_text
