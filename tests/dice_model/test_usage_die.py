from pytest import raises

from dice_model.usage_die import UsageDie, UsageResult, parse

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

# A roll of 1/2 downgrades a UsageDie
def test_usagedie_downgrade(mock_rng):
    die = UsageDie(6, 4)
    result_1 = die.use(rng=mock_rng(1))
    assert result_1.face == 1
    assert result_1.sides_before == 6
    assert result_1.sides_after == 4
    assert result_1.downgraded
    assert not result_1.exhausted
    assert die.position == 1
    result_2 = die.use(rng=mock_rng(2))
    assert result_2.face == 2
    assert result_2.sides_before == 4
    assert result_2.sides_after is None
    assert result_2.downgraded
    assert result_2.exhausted

# An exhausted UsageDie cannot be rolled
def test_usagedie_exhausted(mock_rng):
    die = UsageDie(4)
    result = die.use(rng=mock_rng(1))
    with raises(ValueError):
        die.use()

# You can generate a UsageDie from string syntax
def test_parsing_usagedie_string_syntax():
    assert parse("u6") == UsageDie(6, 4)
    assert parse("u20") == UsageDie(20, 12, 10, 8, 6, 4)
    assert parse("u6p1") == UsageDie(6, 4, 20, 12, 10, 8, 6, 4)
    assert parse("z14") == UsageDie(14, 12, 10, 8, 7, 6, 5, 4)
    assert parse("z4p2") == UsageDie(4, 20, 16, 14, 12, 10, 8, 7, 6, 5, 4, 20, 16, 14, 12, 10, 8, 7, 6, 5, 4)

# A UsageDie can return its own string syntax
def test_generating_usagedie_string_syntax():
    assert UsageDie(6, 4).to_string() == "u6"
    assert UsageDie(20, 12, 10, 8, 6, 4).to_string() == "u20"
    assert UsageDie(6, 4, 20, 12, 10, 8, 6, 4).to_string() == "u6p1"
    assert UsageDie(14, 12, 10, 8, 7, 6, 5, 4).to_string() == "z14"
    assert UsageDie(4, 20, 16, 14, 12, 10, 8, 7, 6, 5, 4, 20, 16, 14, 12, 10, 8, 7, 6, 5, 4).to_string() == "z4p2"
    
    
