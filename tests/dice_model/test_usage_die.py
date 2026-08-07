from pytest import raises

from dice_model.usage_die import UsageDie

# UsageDie can be created
def test_usagedie_creation():
    arrows = UsageDie(10, 8, 6, 4)
    level_10_magic_user_spells_per_day = UsageDie(10, 8, 6, 4, 20, 12, 10, 8, 6, 4)
    level_10_warlock_spells_per_day = UsageDie(20, 16, 14, 12, 10, 8, 7, 6, 5, 4)

# Invalid UsageDie raises errors
def test_usagedie_validation():
    with raises(ValueError):
        UsageDie()

# UsageDie is used and returns a UsageResult
def test_usagedie_use():
    die = UsageDie(6, 4)
    result = die.use()
    assert result.face in {1, 2, 3, 4, 5, 6}
    assert result.sides_before == 6
    assert result.sides_after == 4 if result.face in {1, 2} else result.sides_after == 6
    assert result.downgraded if result.sides_after == 4 else not result.downgraded
    assert not result.exhausted
    assert die.position == 0 if result.sides_after == 6 else die.position == 1



