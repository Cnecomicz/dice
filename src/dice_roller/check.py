from dataclasses import dataclass

from dice_model.dice import Dice
from dice_roller.rng import Rng
from dice_roller.roll import roll

D20 = Dice(sides=20)

@dataclass(frozen=True)
class CheckResult:
    """The outcome of a check attempt.

    Attributes:
        rolls (tuple[int]): Every d20 rolled for the check.
        lower_bound (int): The lower bound; success requires a roll strictly
            above it.
        upper_bound (int): The upper bound; success requires a roll strictly
            below it.
        advantage (int): The signed advantage; success with advantage (>=0)
            requires any roll to succeed; success with disadvantage (<0)
            requires all rolls to succeed.
        success (bool): Whether the check passed.
    """

    rolls: tuple[int, ...]
    lower_bound: int
    upper_bound: int
    advantage: int
    success: bool

    def __bool__(self) -> bool:
        return self.success

def check_above(
    above: int, 
    *,
    advantage: int = 0, 
    tie_succeeds: bool = False, 
    rng: Rng | None = None
) -> CheckResult:
    """Syntactic sugar for thread_the_needle(above, 21), modulo tie_succeeds.

    Args:
        above (int): The lower bound for success.
        advantage (int): The signed advantage. Default 0. A 0 rolls once
            and represents no advantage or disadvantage. A positive value,
            a, rolls a+1 dice, succeeds when any of them succeed, and
            represents advantage. A negative value, d, rolls -d+1 dice,
            succeeds when all of them succeed, and represents disadvantage.
        tie_succeeds (bool): Whether the lower bound "above" counts as success.
        rng (Rng): The randomness source. Defaults to default_rng().

    Returns:
        CheckResult: A class describing the attempt.
    """
    lower_bound = above - 1 if tie_succeeds else above
    return thread_the_needle(
        above=lower_bound, below=21, advantage=advantage, rng=rng
    )

def check_below(
    below: int, 
    *,
    advantage: int = 0, 
    tie_succeeds: bool = False, 
    rng: Rng | None = None
) -> CheckResult:
    """Syntactic sugar for thread_the_needle(0, below), modulo tie_succeeds.

    Args:
        below (int): The upper bound for success.
        advantage (int): The signed advantage. Default 0. A 0 rolls once
            and represents no advantage or disadvantage. A positive value,
            a, rolls a+1 dice, succeeds when any of them succeed, and
            represents advantage. A negative value, d, rolls -d+1 dice,
            succeeds when all of them succeed, and represents disadvantage.
        tie_succeeds (bool): Whether the upper bound "below" counts as success.
        rng (Rng): The randomness source. Defaults to default_rng().

    Returns:
        CheckResult: A class describing the attempt.
    """
    upper_bound = below + 1 if tie_succeeds else below
    return thread_the_needle(
        above=0, below=upper_bound, advantage=advantage, rng=rng
    )

def thread_the_needle(
    above: int, below: int, *, advantage: int = 0, rng: Rng | None = None
) -> CheckResult:
    """Roll a d20 and succeed when it lands strictly between two bounds.

    Args:
        above (int): The lower bound. Success requires the roll to be greater
            than this value.
        below (int): The upper bound. Success requires the roll to be less
            than this value.
        advantage (int): The signed advantage. Default 0. A 0 rolls once
            and represents no advantage or disadvantage. A positive value,
            a, rolls a+1 dice, succeeds when any of them succeed, and
            represents advantage. A negative value, d, rolls -d+1 dice,
            succeeds when all of them succeed, and represents disadvantage.
        rng (Rng): : The randomness source. Defaults to default_rng().

    Returns:
        CheckResult: A class describing the attempt.
    """
    attempts = abs(advantage) + 1
    rolls = tuple(roll(dice=D20, rng=rng).face for i in range(attempts))
    individual_successes = [above < face < below for face in rolls]
    success = (
        any(individual_successes) 
        if advantage >= 0 
        else all(individual_successes)
    )
    return CheckResult(
        rolls=rolls,
        lower_bound=above,
        upper_bound=below,
        advantage=advantage,
        success=success
    )

