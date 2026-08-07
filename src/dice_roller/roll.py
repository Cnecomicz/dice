from dataclasses import dataclass

from dice_model.dice import Dice
from dice_roller.rng import default_rng, Rng

@dataclass(frozen=True)
class RollResult:
    """The outcome of rolling a Dice.

    Attributes:
        dice (Dice): The Dice that was rolled.
        faces (tuple[int, ...]): Every face rolled, in the order they were
            rolled.
        kept (tuple[int, ...]): The faces that counted toward the total;
            the highest Dice.keep of them if keep was not None, or else
            all faces.
        total (int): The resulting roll. 
            (total = sum(kept) * Dice.multiplier + Dice.summand)
    """
    dice: Dice
    faces: tuple[int, ...]
    kept: tuple[int, ...]
    total: int

    @property
    def face(self) -> int:
        """If only one die is rolled, this is the face it rolled.

        Raises:
            ValueError: If the roll produced anything other than one face.
        """
        if len(self.faces) != 1:
            raise ValueError(
                "RollResult.face is only defined for a single die roll; "
                f"this roll has {len(self.faces)} faces."
            )
        return self.faces[0]

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
    all_rolls = tuple(rng.randint(1, dice.sides) for die in range(quantity))
    if dice.keep is None:
        kept = all_rolls
    else:
        kept = sorted(all_rolls, reverse=True)[: dice.keep]
    total = sum(kept) * dice.multiplier + dice.summand
    return RollResult(
        dice=dice, faces=all_rolls, kept=kept, total=total
    )