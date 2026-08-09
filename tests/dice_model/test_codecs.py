from dice_model.codecs import parse
from dice_model.dice import Dice

# You can generate Dice from string syntax
def test_parsing_dice_string_syntax():
    assert parse("d20") == Dice(sides=20)
    assert parse("3d6") == Dice(quantity=3, sides=6)
    assert parse("3d20k1") == Dice(quantity=3, sides=20, keep=1)
    assert parse("d4+2") == Dice(sides=4, summand=2)
    assert parse("3d6*10") == Dice(quantity=3, sides=6, multiplier=10)
    assert parse("l*d6") == Dice(sides=6, per_level=True)
    assert parse("l*2d6k1*3+2") == Dice(quantity=2, sides=6, keep=1, multiplier=3, summand=2, per_level=True)

# You can generate a UsageDie from string syntax
def test_parsing_usagedie_string_syntax():
    assert parse("u6").chain == (6, 4)
    assert parse("u20").chain == (20, 12, 10, 8, 6, 4)
    assert parse("u6p1").chain == (6, 4, 20, 12, 10, 8, 6, 4)
    assert parse("z14").chain ==(14, 12, 10, 8, 7, 6, 5, 4)
    assert parse("z4p2").chain == (4, 20, 16, 14, 12, 10, 8, 7, 6, 5, 4, 20, 16, 14, 12, 10, 8, 7, 6, 5, 4)
