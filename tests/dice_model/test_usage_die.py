from pytest import raises

from dice_model.usage_die import UsageDie

# UsageDie can be created.
def test_usagedie_creation():
    arrows = UsageDie(10, 8, 6, 4)
    level_10_magic_user_spells_per_day = UsageDie(10, 8, 6, 4, 20, 12, 10, 8, 6, 4)
    level_10_warlock_spells_per_day = UsageDie(20, 16, 14, 12, 10, 8, 7, 6, 5, 4)

# Invalid UsageDie raises errors
def test_usagedie_validation():
    with raises(ValueError):
        UsageDie()