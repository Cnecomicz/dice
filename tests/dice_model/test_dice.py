from dice_model.dice import Dice

# Dice can be created. NB: I'm creating examples straight from the TTRPG
# which demonstrate the need for these attrs
def test_dice_creation():
    extreme_character_creation = Dice(quantity=3, sides=20, keep=1)
    cleric_spells_gained = Dice(sides=4, summand=2)
    starting_gold = Dice(quantity=3, sides=6, multiplier=10)
    elemental_blast_spell_damage = Dice(sides=6, per_level=True)
