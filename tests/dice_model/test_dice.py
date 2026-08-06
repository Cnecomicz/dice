from pytest import raises

from dice_model.dice import Dice, parse

# Dice can be created. NB: I'm creating examples straight from the TTRPG
# which demonstrate the need for these attrs
def test_dice_creation():
    extreme_character_creation = Dice(quantity=3, sides=20, keep=1)
    cleric_spells_gained = Dice(sides=4, summand=2)
    starting_gold = Dice(quantity=3, sides=6, multiplier=10)
    elemental_blast_spell_damage = Dice(sides=6, per_level=True)

# Invalid Dice raise errors
def test_dice_validation():
    with raises(ValueError):
        Dice(quantity=0, sides=6)
    with raises(ValueError):
        Dice(sides=0)
    with raises(ValueError):
        Dice(quantity=2, sides=6, keep=3)
    with raises(ValueError):
        Dice(quantity=2, sides=6, keep=0)
    with raises(ValueError):
        Dice(sides=6, multiplier=0)

# You can generate Dice from string syntax
def test_parsing_dice_string_syntax():
    assert parse("d20") == Dice(sides=20)
    assert parse("3d6") == Dice(quantity=3, sides=6)
    assert parse("3d20k1") == Dice(quantity=3, sides=20, keep=1)
    assert parse("d4+2") == Dice(sides=4, summand=2)
    assert parse("3d6*10") == Dice(quantity=3, sides=6, multiplier=10)
    assert parse("l*d6") == Dice(sides=6, per_level=True)
    assert parse("l*2d6k1*3+2") == Dice(quantity=2, sides=6, keep=1, multiplier=3, summand=2, per_level=True)

# A Dice can return its own string syntax
def test_generating_dice_string_syntax():
    assert Dice(sides=20).to_string() == "d20"
    assert Dice(quantity=3, sides=6).to_string() == "3d6"
    assert Dice(quantity=3, sides=20, keep=1).to_string() == "3d20k1"
    assert Dice(sides=4, summand=2).to_string() == "d4+2"
    assert Dice(quantity=3, sides=6, multiplier=10).to_string() == "3d6*10"
    assert Dice(sides=6, per_level=True).to_string() == "l*d6"
    assert Dice(quantity=2, sides=6, keep=1, multiplier=3, summand=2, per_level=True).to_string() == "l*2d6k1*3+2"