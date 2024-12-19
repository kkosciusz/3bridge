import pytest
from bridge.hand import Card, Hand, Rank, Suit


def test_empty_hand_has_len_0():
    hand = Hand()
    assert len(hand) == 0


def test_after_adding_card_to_empty_hand_card_is_in_hand():
    hand = Hand()
    card = Card(Suit.SPADE, Rank.ACE)
    hand.add(card)
    assert card in hand


def test_adding_a_card_to_a_hand_twice_throws():
    hand = Hand()
    card = Card(Suit.SPADE, Rank.ACE)
    hand.add(card)
    with pytest.raises(ValueError, match=r".* already in hand"):
        hand.add(card)


def test_comparing_cards_for_equality_is_supported():
    card1 = Card(Suit.SPADE, Rank.ACE)
    card2 = Card(Suit.HEART, Rank.ACE)
    card3 = Card(Suit.HEART, Rank.KING)
    card4 = Card(Suit.SPADE, Rank.ACE)

    assert card1 == card4
    assert card1 != card2
    assert card2 != card3
    assert card3 != card4


def test_given_a_card_can_compute_hcl_value():
    ace = Card(Suit.HEART, Rank.ACE)
    king = Card(Suit.SPADE, Rank.KING)
    queen = Card(Suit.DIAMOND, Rank.QUEEN)
    jack = Card(Suit.CLUB, Rank.JACK)
    ten = Card(Suit.CLUB, Rank.TEN)
    cards = (ace, king, queen, jack, ten)
    assert [card.hcl() for card in cards] == [4, 3, 2, 1, 0]


def test_given_a_hand_can_compute_hcl_value():
    ace = Card(Suit.HEART, Rank.ACE)
    king = Card(Suit.SPADE, Rank.KING)
    queen = Card(Suit.DIAMOND, Rank.QUEEN)
    jack = Card(Suit.CLUB, Rank.JACK)
    ten = Card(Suit.CLUB, Rank.TEN)
    cards = (ace, king, queen, jack, ten)
    hand = Hand(cards)
    assert hand.hcl() == 10


@pytest.mark.parametrize(
    ("cards", "expected"),
    [
        ([], '...'),
        (['SA'], 'A...'),
        (['HA'], '.A..'),
        (['DA'], '..A.'),
        (['CA'], '...A'),
        (['SA', 'HK'], 'A.K..'),
        (['HA', 'SK'], 'K.A..'),
        (['DA', 'CK'], '..A.K'),
        (['CA', 'DK'], '..K.A'),
        (['CK', 'CA', 'CJ', 'CQ'], '...AKQJ'),
    ],
)
def test_can_output_hand_as_string(cards, expected):
    hand = Hand({Card.from_text(t) for t in cards})
    assert hand.as_text() == expected


def test_card_ranks_are_properly_ordered():
    unordered = [
        Rank.QUEEN,
        Rank.TWO,
        Rank.KING,
        Rank.SIX,
        Rank.JACK,
        Rank.ACE,
        Rank.TEN,
    ]
    ordered = [
        Rank.TWO,
        Rank.SIX,
        Rank.TEN,
        Rank.JACK,
        Rank.QUEEN,
        Rank.KING,
        Rank.ACE,
    ]
    assert ordered == sorted(unordered)


def test_card_suits_are_properly_ordered():
    unordered = [Suit.HEART, Suit.CLUB, Suit.SPADE, Suit.DIAMOND]
    ordered = [Suit.CLUB, Suit.DIAMOND, Suit.HEART, Suit.SPADE]
    assert ordered == sorted(unordered)


@pytest.mark.parametrize("rank_text", "A K Q J 10 9 8 7 6 5 4 3 2".split())
@pytest.mark.parametrize("suit_text", "S H D C".split())
def test_text_to_card_and_back_gives_same_text(suit_text, rank_text):
    card_text = suit_text + rank_text
    card = Card.from_text(card_text)
    assert card.as_text() == card_text


@pytest.mark.parametrize(
    "hand_text",
    [
        "...",
        "A...",
        ".A..",
        "..A.",
        "...A",
        "A.K..",
        "K.A..",
        "..A.K",
        "..K.A",
        "AK.QJ.109.876",
        "A108.A108.A108.A108",
    ],
)
def test_hand_text_to_hand_and_back_gives_same_text(hand_text):
    hand = Hand.from_text(hand_text)
    assert hand.as_text() == hand_text


def test_parsing_hand_from_text_hand_1():
    hand_text = "AKQ.J10.98765.AKQ"
    hand = Hand.from_text(hand_text)
    card_texts = "SA SK SQ HJ H10 D9 D8 D7 D6 D5 CA CK CQ".split()
    expected_cards = [Card.from_text(c) for c in card_texts]
    assert len(hand) == len(expected_cards)
    assert all(card in expected_cards for card in hand)


@pytest.mark.parametrize(
    "hand_text",
    [
        "AA...",
        ".AA..",
        "..AA.",
        "...AA",
    ],
)
def test_creating_hand_from_text_with_duplicate_cards_of_one_suit_throw(hand_text):
    with pytest.raises(ValueError, match=r".* already in hand"):
        Hand.from_text(hand_text)


@pytest.mark.parametrize(
    "hand_text",
    [
        "z...",
        "11...",
        "T...",
        "121...",
    ],
)
def test_creating_hand_from_text_with_invalid_card_ranks_throw(hand_text):
    with pytest.raises(ValueError, match=r"unknown card rank"):
        Hand.from_text(hand_text)


@pytest.mark.parametrize(
    "hand_text",
    [
        "",
        ".",
        "..",
        "....",
        "A.A.A.A.A",
    ],
)
def test_creating_hand_form_text_with_invalid_number_of_suits_throw(hand_text):
    with pytest.raises(ValueError, match=r"expecting exactly 4 suits"):
        Hand.from_text(hand_text)
