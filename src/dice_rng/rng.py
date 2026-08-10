from random import Random
from typing import Protocol, runtime_checkable

@runtime_checkable
class Rng(Protocol):
    """The seam roll depends on to obtain randomness.

    Any object exposing a randint() method can be supplied whenever Rng
    is required. This allows for seeding, testing/debugging and
    reproducibility, independent rng streams, save/load, etc.
    """

    def randint(self, low: int, high: int) -> int:
        """Return a random integer n such that low <= n <= high.

        Args:
            low (int): The lower bound.
            high (int): The upper bound.

        Returns:
            int: A value between low and high, inclusive.
        """
        ...

class DefaultRng:
    """This library's provided default Rng.

    Attributes:
        seed (int | None): An optional seed. When left None, the sequence
            of rolls is nondeterministic.
    """

    def __init__(self, seed: int | None = None) -> None:
        self.random = Random(seed)

    def randint(self, low: int, high: int) -> int:
        """Return a random integer n such that low <= n <= high, using the
        random python library.

        Args:
            low (int): The lower bound.
            high (int): The upper bound.

        Returns:
            int: A value between low and high, inclusive.
        """
        return self.random.randint(low, high)

singleton = DefaultRng()

def default_rng() -> DefaultRng:
    """Return the shared process-wide Rng.

    This is the source used by roll() and UsageDie.use() when the caller
    does not supply an Rng. It is unseeded and nondeterministic. For
    reproducible or isolated randomness, pass your own Rng explicitly instead
    of relying on this shared instance.
    """
    return singleton