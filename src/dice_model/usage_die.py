from __future__ import annotations
from dataclasses import dataclass

from dice_model.dice import Dice
from dice_roller.rng import Rng
from dice_roller.roll import roll

DOWNGRADE_ON = {1, 2}

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

    def use(self, rng: Rng | None = None) -> UsageResult:
        """Spend the resource; roll the current die and possibly downgrade.

        A roll of 1 or 2 downgrades the usage die one step along its chain,
        which may exhaust it. Any other roll leaves the die where it is.

        Args:
            rng (Rng): The randomness source. Defaults to the default_rng().

        Returns:
            A UsageResult recording what happened on this use.
        """
        if self.exhausted:
            raise ValueError("Cannot use an exhausted usage die.")
        sides_before = self.chain[self.position]
        face = roll(dice=Dice(sides=sides_before), rng=rng)
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

def parse(dice_syntax: str) -> UsageDie:
    pass