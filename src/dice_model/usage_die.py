from __future__ import annotations
from dataclasses import dataclass

from dice_model.dice import Dice
from dice_roller.rng import Rng
from dice_roller.roll import roll

DOWNGRADE_ON = {1, 2}
REGULAR_LADDER = (20, 12, 10, 8, 6, 4)
ZOCCHI_LADDER = (20, 16, 14, 12, 10, 8, 7, 6, 5, 4)

class UsageDie:
    """A usage die that wears down as its resource is spent.

    Attributes:
        chain (tuple[int, ...]): The ordered side counts that the usage
            die steps through. Must be nonempty.
        position (int): The index in chain of the die currently in play,
            starting at 0. If position == len(chain), the usage die is
            exhausted.
    """

    def __init__(self, *chain: int) -> None:
        if not chain:
            raise ValueError(
                "A usage die needs at least one die in its chain."
            )
        self.chain = chain
        self.position = 0

    @property
    def current_sides(self) -> int | None:
        """The number of sides of the current die, or None if exhausted."""
        return self.chain[self.position] if not self.exhausted else None

    @property
    def exhausted(self) -> bool:
        """Whether the resource has been used up."""
        return self.position >= len(self.chain)

    def to_string(self) -> str:
        """Return the dice syntax string notation for this UsageDie.

        Dice syntax is determined by matching the chain to either the regular
        or the Zocchi ladders. A valid chain begins at some point in the
        ladder (not necessarily the start) and follows it exactly to the
        end of the ladder. It then has 0 or more full copies of the ladder,
        indicating a prestiged UsageDie. 

        Returns:
            str: A formatted dice syntax string.

        Raises:
            ValueError: If the chain does not follow the regular or Zocchi
                ladder and thus has no canonical shorthand.
        """
        for ladder in (REGULAR_LADDER, ZOCCHI_LADDER):
            try:
                start = ladder.index(self.chain[0])
            except ValueError:
                continue
            suffix = ladder[start:]
            if self.chain[:len(suffix)] != suffix:
                continue
            tail = self.chain[len(suffix):]
            if len(tail) % len(ladder) != 0:
                continue
            prestige = len(tail) // len(ladder)
            if tail != ladder * prestige:
                continue
            dice_syntax = ""
            dice_syntax += "u" if ladder == REGULAR_LADDER else "z"
            dice_syntax += str(self.chain[0])
            dice_syntax += f"p{prestige}" if prestige > 0 else ""
            return dice_syntax
        raise ValueError(
            f"Chain {self.chain} does not conform to a canonical dice syntax."
        )

    def use(self, rng: Rng | None = None) -> UsageResult:
        """Spend the resource; roll the current die and possibly downgrade.

        A roll of 1 or 2 downgrades the usage die one step along its chain,
        which may exhaust it. Any other roll leaves the die where it is.

        Args:
            rng (Rng): The randomness source. Defaults to default_rng().

        Returns:
            A UsageResult recording what happened on this use.
        """
        if self.exhausted:
            raise ValueError("Cannot use an exhausted usage die.")
        sides_before = self.chain[self.position]
        face = roll(dice=Dice(sides=sides_before), rng=rng).face
        downgraded = face in DOWNGRADE_ON
        if downgraded:
            self.position += 1
        return UsageResult(
            face=face,
            sides_before=sides_before,
            sides_after=self.current_sides,
            downgraded=downgraded,
            exhausted=self.exhausted
        )

@dataclass(frozen=True)
class UsageResult:
    """A record of a single use of a UsageDie.

    Reports what happened on one use. The UsageDie itself keeps track of
    its own state and updates itself; this is just to record a single use()
    call.

    Attributes:
        face (int): The face rolled on the die.
        sides_before (int): The number of sides prior to use() call.
        sides_after (int | None): The number of sides after use() call.
        downgraded (bool): Whether the use() call downgraded the UsageDie.
        exhausted (bool): Whether the use() call exhausted the UsageDie.
    """

    face: int
    sides_before: int
    sides_after: int | None
    downgraded: bool
    exhausted: bool
