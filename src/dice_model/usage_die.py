class UsageDie:
    """A usage die that wears down as its resource is spent.

    Attributes:
        chain: The ordered side counts that the usage die steps through.
            Must be nonempty.
        index: The position in chain of the die currently in play, starting
            at 0. If index == len(chain), the usage die is exhausted.
    """

    def __init__(self, *chain: int) -> None:
        if not chain:
            raise ValueError(
                "A usage die needs at least one die in its chain."
            )
        self.chain = chain
        self.position = 0
