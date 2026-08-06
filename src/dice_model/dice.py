from dataclasses import dataclass

@dataclass(frozen=True)
class Dice:
    """A set of same-sided dice to roll, with potential modifiers.

    Attributes:
        sides: How many sides each die has. Must be at least 1.
        quantity: How many dice to roll. Must be at least 1. Default 1.
        keep: How many of the highest rolls to keep. Must be between 1 and
            quantity, inclusive. Default None (a sentinel meaning to keep
            all rolled dice).
        summand: An amount added to the total. Default 0.
        multiplier: An amount multiplied by the total. Default 1. Note:
            between summand and multipler, multiplication occurs before 
            addition.
        per_level: Indicate whether the amount of dice to roll scales
            multiplicatively with the character's level. Default False.
    """
    
    sides: int
    quantity: int = 1
    keep: int | None = None
    summand: int = 0
    multiplier: int = 1
    per_level: bool = False

