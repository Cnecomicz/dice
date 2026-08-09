from dataclasses import dataclass

@dataclass(frozen=True)
class Dice:
    """A set of same-sided dice to roll, with potential modifiers.

    Attributes:
        quantity (int): How many dice to roll. Must be at least 1. Default
            1.
        sides (int): How many sides each die has. Must be at least 1. Default 
            0, because we want the attr order to match dice string syntax
            but also want require the caller to provide a number of sides.
        keep (int | None): How many of the highest rolls to keep. Must be
            between 1 and quantity, inclusive. Default None (a sentinel
            meaning to keep all rolled dice).
        multiplier (int): An amount multiplied by the total. Default 1.
        summand (int): An amount added to the total. Default 0. Note: between
            summand and multipler, multiplication occurs before addition.
        per_level (bool): Indicate whether the amount of dice to roll scales
            multiplicatively with the character's level. Default False.
    """

    quantity: int = 1
    sides: int = 0
    keep: int | None = None
    multiplier: int = 1
    summand: int = 0
    per_level: bool = False

    def __post_init__(self) -> None:
        if self.quantity < 1:
            raise ValueError(
                f"Quantity is {self.quantity} but must be at least 1."
            )
        if self.sides < 1:
            raise ValueError(
                f"Sides is {self.sides} but must be at least 1."
            )
        if (
            self.keep is not None 
            and (self.keep < 1 or self.keep > self.quantity)
        ):
            raise ValueError(
                f"Keep is {self.keep} but must be at least 1 and at most "
                f"quantity={self.quantity}."
            )
        if self.multiplier == 0:
            raise ValueError("Multiplier cannot be 0.")

    def to_string(self) -> str:
        """Return the dice syntax string notation for this Dice.

        Returns:
            str: A formatted dice syntax string.
        """
        dice_syntax = ""
        dice_syntax += "l*" if self.per_level else ""
        dice_syntax += f"{self.quantity}" if self.quantity > 1 else ""
        dice_syntax += f"d{self.sides}"
        dice_syntax += f"k{self.keep}" if self.keep is not None else ""
        dice_syntax += f"*{self.multiplier}" if self.multiplier != 1 else ""
        dice_syntax += f"{self.summand:+d}" if self.summand != 0 else ""
        return dice_syntax

