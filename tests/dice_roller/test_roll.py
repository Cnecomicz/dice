from dice_model.dice import Dice
from dice_roller.roll import RollResult, roll

# roll returns a RollResult
def test_rolling_a_die(mock_rng):
    result = roll(Dice(sides=6), rng=mock_rng(4))
    assert result.dice == Dice(sides=6)
    assert result.faces == (4,)
    assert result.kept == (4,)
    assert result.total == 4
