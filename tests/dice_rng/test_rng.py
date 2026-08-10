from dice_rng.rng import DefaultRng, Rng

# The seam is well-defined
def test_default_rng_is_an_rng_and_anything_with_randint_is_an_rng():
    assert isinstance(DefaultRng(), Rng)
    class DumbRng:
        def randint(self, low, high):
            return low
    assert isinstance(DumbRng(), Rng)

# Randomness respects bounds
def test_randint_between_low_and_high():
    rng = DefaultRng()
    for i in range(1000):
        value = rng.randint(1, 100)
        assert 1 <= value <= 100
    four = rng.randint(4, 4)
    assert four == 4

# Seeding works
def test_same_seed_produces_same_sequence_but_different_seeds_generally_differ():
    rng_1 = DefaultRng(seed=0)
    rng_2 = DefaultRng(seed=0)
    rng_3 = DefaultRng(seed=1)
    rng_4 = DefaultRng(seed=2)
    deck_1 = []
    deck_2 = []
    deck_3 = []
    deck_4 = []
    for deck, rng in ((deck_1, rng_1), (deck_2, rng_2), (deck_3, rng_3), (deck_4, rng_4)):
        while len(deck) < 52:
            n = rng.randint(1, 52)
            if n not in deck:
                deck.append(n)
    assert deck_1 == deck_2
    assert deck_3 != deck_4