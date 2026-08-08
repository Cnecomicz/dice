from dice_roller.check import thread_the_needle

# You can thread the needle
def test_thread_the_needle(mock_rng):
    for roll in range(1, 21):
        result = thread_the_needle(above=5, below=15, rng=mock_rng(roll))
        assert result.rolls == (roll,)
        assert result.lower_bound == 5
        assert result.upper_bound == 15
        assert result.advantage == 0
        assert result.success if roll in {6, 7, 8, 9, 10, 11, 12, 13, 14} else not result.success
    for advantage in range(0, 3):
        advantage_rolls = [8, 9, 10]
        advantage_attempt = advantage_rolls[:advantage+1]
        advantage_result = thread_the_needle(above=8, below=12, advantage=advantage, rng=mock_rng(*advantage_attempt))
        assert advantage_result.advantage == advantage
        assert advantage_result.success if advantage in {1, 2} else not advantage_result.success
    for disadvantage in range(-2, 1):
        disadvantage_rolls = [10, 9, 8]
        disadvantage_attempt = disadvantage_rolls[:-disadvantage+1]
        disadvantage_result = thread_the_needle(above=8, below=12, advantage=disadvantage, rng=mock_rng(*disadvantage_attempt))
        assert disadvantage_result.advantage == disadvantage
        assert disadvantage_result.success if disadvantage in {-1, 0} else not disadvantage_result.success

