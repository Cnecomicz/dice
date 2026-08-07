from dataclasses import dataclass
from re import compile, IGNORECASE, VERBOSE

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
                f"{self.quantity=}."
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


def parse(dice_syntax: str) -> Dice:
    """Build a Dice from its string notation.

    Supported formats:
    - "dS": Dice with S sides. 
        Example: "d20" ↦ Dice(sides=20)
    - "QdS": Dice with Q quantity and S sides. 
        Example: "3d6" ↦ Dice(quantity=3, sides=6)
    - "QdSkK": Dice with Q quantity, S sides, and K keep.
        Example: "3d20k1" ↦ Dice(quantity=3, sides=20, keep=1)
    - "dS+A": Dice with S sides and A summand.
        Example: "d4+2" ↦ Dice(sides=4, summand=2)
    - "QdS*M": Dice with Q quantity, S sides, and M multiplier.
        Example: "3d6*10" ↦ Dice(quantity=3, sides=6, multiplier=10)
    - "l*dS": Dice with S sides and True per_level.
        Example: "l*d6" ↦ Dice(sides=6, per_level=True)
    All syntax can be used at once:
        ""l*2d6k1*3+2" ↦ Dice(
            quantity=2, sides=6, keep=1, 
            multiplier=3, summand=2, per_level=True
        )

    Args:
        dice_syntax (str): A valid dice syntax string.

    Returns:
        Dice: The described Dice object.

    Raises:
        ValueError: If dice_syntax is not valid dice syntax.
    """
    notation = compile(
        r"""
        ^
        (?P<per_level>l\*)?
        (?P<quantity>\d+)?
        d(?P<sides>\d+)
        (?:k(?P<keep>\d+))?
        (?:\*(?P<multiplier>\d+))?
        (?P<summand>[+-]\d+)?
        $
        """,
        IGNORECASE | VERBOSE
    )
    match = notation.fullmatch(dice_syntax)
    if match is None:
        raise ValueError(f"Invalid dice syntax: {dice_syntax!r}.")
    attrs = match.groupdict()
    return Dice(
        quantity=int(attrs["quantity"]) if attrs["quantity"] else 1,
        sides=int(attrs["sides"]) if attrs["sides"] else 0,
        keep=int(attrs["keep"]) if attrs["keep"] else None,
        multiplier=int(attrs["multiplier"]) if attrs["multiplier"] else 1,
        summand=int(attrs["summand"]) if attrs["summand"] else 0,
        per_level=True if attrs["per_level"] is not None else False
    )

