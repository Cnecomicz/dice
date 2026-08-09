from pytest import raises

from dice_model.dice import Dice
from dice_roller.roll import RollResult, roll

# roll returns a RollResult
def test_rolling_a_die(mock_rng):
    result = roll(Dice(sides=6), rng=mock_rng(4))
    assert result.dice == Dice(sides=6)
    assert result.faces == (4,)
    assert result.kept == (4,)
    assert result.total == 4

# face is only valid for single die rolls and can be distinct from total
def test_face_alias(mock_rng):
    result_1 = roll(Dice(quantity=3, sides=6))
    with raises(ValueError):
        result_1.face
    result_2 = roll(Dice(sides=6, multiplier=10, summand=1), rng=mock_rng(4))
    assert result_2.face == 4
    assert result_2.total == 41

# RollResult in int contexts acts as its total
def test_result_converts_to_total(mock_rng):
    result = roll(Dice(quantity=3, sides=10, keep=2))
    assert int(result) == result.total

# All the roll operations work: you sum, keep, multiply, add, level scale
def test_roll_arithmetic(mock_rng):
    result_1 = roll(Dice(quantity=3, sides=6), rng=mock_rng(1, 5, 3))
    assert result_1.faces == (1, 5, 3)
    assert result_1.kept == (1, 5, 3)
    assert result_1.total == 9
    result_2 = roll(Dice(quantity=3, sides=20, keep=1), rng=mock_rng(7, 19, 12))
    assert result_2.faces == (7, 19, 12)
    assert result_2 .kept == (19,)
    assert result_2.total == 19
    result_3 = roll(Dice(quantity=3, sides=6, multiplier=10), rng=mock_rng(2, 4, 6))
    assert result_3.total == 120
    result_4 = roll(Dice(quantity=2, sides=8, summand=1), rng=mock_rng(3, 5))
    assert result_4.total == 9
    result_5 = roll(Dice(sides=6, multiplier=10, summand=1), rng=mock_rng(2))
    assert result_5.total == 21
    result_6 = roll(Dice(sides=6, per_level=True), level=3, rng=mock_rng(1, 2, 3))
    assert result_6.faces == (1, 2, 3)
    assert result_6.total == 6
    result_7 = roll(Dice(quantity=2, sides=6), level=5, rng=mock_rng(4, 4))
    assert result_7.faces == (4, 4)