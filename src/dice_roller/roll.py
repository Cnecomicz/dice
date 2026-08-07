from random import randint

from dice_model.dice import Dice

def roll(dice: Dice, level: int = 1) -> int:
    """Roll the set of dice and return the result.

    Args:
        dice (Dice): The description of what to roll.
        level (int): The character level, relevant if dice.per_level == True.

    Returns:
        int: The resulting roll.
    """
    quantity = dice.quantity * (level if dice.per_level else 1)
    all_rolls = (randint(1, dice.sides) for die in range(quantity))
    if dice.keep is None:
        kept = all_rolls
    else:
        kept = sorted(all_rolls, reverse=True)[: dice.keep]
    total = sum(kept) * dice.multiplier + dice.summand
    return total