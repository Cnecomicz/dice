from dice_model.dice import Dice
from dice_roller.rng import default_rng, Rng

class RollResult:
    pass

def roll(dice: Dice, level: int = 1, rng: Rng | None = None) -> int:
    """Roll the set of dice and return the result.

    Args:
        dice (Dice): The description of what to roll.
        level (int): The character level, relevant if dice.per_level == True.
        rng (Rng): The randomness source. Defaults to the default_rng().

    Returns:
        int: The resulting roll.
    """
    rng = rng if rng is not None else default_rng()
    quantity = dice.quantity * (level if dice.per_level else 1)
    all_rolls = (rng.randint(1, dice.sides) for die in range(quantity))
    if dice.keep is None:
        kept = all_rolls
    else:
        kept = sorted(all_rolls, reverse=True)[: dice.keep]
    total = sum(kept) * dice.multiplier + dice.summand
    return total