from re import compile, IGNORECASE, VERBOSE

from dice_model.dice import Dice
from dice_model.usage_die import REGULAR_LADDER, ZOCCHI_LADDER, UsageDie

DICE_NOTATION = compile(
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

USAGEDIE_NOTATION = compile(
    r"""
    ^
    (?P<zocchi>[uz])
    (?P<sides>\d+)
    (?:p(?P<prestige>\d+))?
    $
    """,
    IGNORECASE | VERBOSE
)

def parse(dice_syntax: str) -> Dice | UsageDie:
    """Build a Dice or UsageDie from its string notation.

    A convenience method / syntactic sugar. Calls parse_dice() or
    parse_usagedie() depending on dice_syntax. See respective docstrings
    for further details.

    Args:
        dice_syntax (str): A valid dice syntax string.

    Returns:
        Dice | UsageDie: The described Dice or UsageDie object.

    Raises:
        ValueError: If dice_syntax is not valid dice syntax.
    """
    try:
        return parse_dice(dice_syntax)
    except ValueError:
        return parse_usagedie(dice_syntax)

def parse_dice(dice_syntax: str) -> Dice:
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
        "l*2d6k1*3+2" ↦ Dice(
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
    match = DICE_NOTATION.fullmatch(dice_syntax)
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

def parse_usagedie(dice_syntax: str) -> UsageDie:
    """Build a UsageDie from its string notation.

    Supported formats:
    - "uS": Non-Zocchi UsageDie with S sides. 
        Example: "u6" ↦ UsageDie(6, 4)
    - "zS": Zocchi UsageDie with S sides. 
        Example: "z6" ↦ UsageDie(6, 5, 4)
    - "uSpP": Non-Zocchi UsageDie with S sides and P prestige.
        Example: "u6p1" ↦ UsageDie(6, 4, 20, 12, 10, 8, 6, 4)
    - "zSpP": Zocchi UsageDie with S sides and P prestige.
        Example: "z6p1" ↦ UsageDie(6, 5, 4, 20, 16, 14, 12, 10, 8, 7, 6, 5, 4)

    Args:
        dice_syntax (str): A valid dice syntax string.

    Returns:
        UsageDie: The described UsageDie object.

    Raises:
        ValueError: If dice_syntax is not valid dice syntax.
    """
    match = USAGEDIE_NOTATION.fullmatch(dice_syntax)
    if match is None:
        raise ValueError(f"Invalid dice syntax: {dice_syntax!r}.")
    attrs = match.groupdict()
    is_zocchi = attrs["zocchi"].lower() == "z"
    ladder = ZOCCHI_LADDER if is_zocchi else REGULAR_LADDER
    sides = int(attrs["sides"])
    if sides not in ladder:
        ladder_name = "Zocchi" if is_zocchi else "regular"
        valid_sides = (
            ", ".join(str(side) for side in ladder[:-1])
            + ", or "
            + str(ladder[-1])
        )
        raise ValueError(
            f"A {ladder_name} usage die must start on one of {valid_sides}, "
            f"but {sides} was provided instead."
        )
    prestige = int(attrs["prestige"]) if attrs["prestige"] else 0
    start = ladder.index(sides)
    chain = ladder[start:] + ladder*prestige
    return UsageDie(*chain)