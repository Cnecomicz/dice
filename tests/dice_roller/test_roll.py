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
def test_result_coerces_to_total(mock_rng):
    hp = 2
    bandages = roll(Dice(sides=4), rng=mock_rng(3))
    hp += bandages
    assert hp == 5
