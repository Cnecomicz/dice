from dice_roller.check import thread_the_needle

# You can thread the needle
def test_thread_the_needle(mock_rng):
    for i in range(1, 21):
        result = thread_the_needle(above=5, below=15, rng=mock_rng(i))
        assert result.rolls == (i,)
        assert result.lower_bound == 5
        assert result.upper_bound == 15
        assert result.advantage == 0
        assert result.success if i in {5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15} else not result.success
    for j in range(-2, 3):
        all_rolls = [8, 10, 12]
        attempt = rolls[:abs(j)+1]
        result = thread_the_needle(above=9, below=11, rng=mock_rng(attempt))
        assert result.advantage == j
        assert (
            result.success 
            if j >= 0 and any(attempt in {9, 10, 11})
            or j <0 and all(attempt in {9, 10, 11})
            else not result.success
        )

