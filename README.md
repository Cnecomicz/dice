# Dice

A Python toolkit for translating TTRPG dice mechanics generally, and my
homebrew *Gold & Gallows* mechanics specifically, into a video game engine. 
This is intended to support my current game development but has been built 
standalone in order to contain its scope and to allow anyone willing to use 
my conventions to adopt it for their own purposes.

It includes:

* A dice model which standardizes sets of dice and usage dice.
* A dice roller which handles rolling dice and returns a verbose description
    of the outcome.
* A dedicated RNG seam for determining roll outcomes, along with a canonical
    default implementation.
* Implementations of check and save mechanics from my TTRPG *Gold & Gallows*.

## Features

* Handle sets of dice:
    * Determine a quantity of same-sided dice to roll.
    * Allows for keeping a subset of the highest rolled faces.
    * Allows for modifying the rolled outcome with scalar multiplication
        and addition.
    * Allows for scaling the quantity of dice rolled dependent on a level
        parameter (for dice quantities that scale with character level).
    * Can output a canonical string syntax that defines the set of dice;
        e.g., "4d6" for four six-sided dice, or "3d10k2" for three ten-sided
        dice, with rolls keeping the highest two dice, among many others.
* Handle a usage die:
    * Define a usage die chain which determines the downgrade path.
    * "Use" the usage die; it downgrades along its chain when rolling a 1
        or 2, and is exhausted when it downgrades off the end of the chain.
    * Can output a canonical string syntax that defines the usage die; e.g.,
        "u12" for a chain `12 -> 10 -> 8 -> 6 -> 4`, or "z4p1" for a chain
        `4 -> 20 -> 16 -> 14 -> 12 -> 10 -> 8 -> 7 -> 6 -> 5 -> 4`.
* Roll dice sets:
    * Receive a verbose outcome of each individual roll, what subset of
        dice were kept, and the total after all modifiers.
    * Contains built-in *Gold & Gallows* d20 checks with upper and lower
        bounds and advantage/disadvantage mechanics.
* Parse string syntax into dice or usage die objects.
* Use provided rng or supply your own.

## Installation

This project requires Python 3.11 or newer.

### Install a released version

To install a specific published release, install it directly from its tag.
For example, to install v1.0.0:

```bash
pip install "git+https://github.com/Cnecomicz/dice.git@v1.0.0"
```

Releases are listed at
[https://github.com/Cnecomicz/dice/releases](https://github.com/Cnecomicz/dice/releases).

### Install from source

To work from the latest source, after downloading this project off of
[https://github.com/Cnecomicz/dice](https://github.com/Cnecomicz/dice), 
install it in the terminal using pip:

```bash
pip install -e .
```

You can also install this project with additional development tools:

```bash
pip install -e ".[dev]"
```

The additional dev dependencies are pytest, pytest-cov, pytest-testmon, 
and pytest-xdist, and are used for running the pytest suite.

## Quick start

### Game engine usage

The following are pseudo-real-world examples of how the tools this project
provides could be used in a game engine. The examples are modeled off of
specific use cases that occur in my *Gold & Gallows* TTRPG, but in general
need not be restricted to only this ruleset, unless specifically are called
out as such.

#### Defining sets of dice and usage dice

Dice can be defined directly via the class `Dice` or by inputting dice string
syntax into the `parse` function. Dice syntax must conform to the following
form:

```
[l*] [quantity] d sides [k keep] [* multiplier] [+/- summand]
```

* `l*`: an optional indicator that the dice quantity scales multiplicatively
    with character level.
* `quantity`: the quantity of dice to roll. If omitted, the quantity will
    be 1.
* `d`: signals the syntax represents ordinary `Dice`.
* `sides`: the number of sides each die has.
* `k keep`: an optional indicator that you should only keep the `keep` highest
    dice out of all rolled. `keep` must be at least 1 and at most `quantity`.
* `* multipler`: an optional indicator to multiply the result by the value
    `multiplier`.
* `+/- summand`: an optional indicator to add or subtract the value `summand`
    to the result.

```python
from dice_model import Dice, parse

extreme_character_creation = Dice(quantity=3, sides=20, keep=1)
# OR
extreme_character_creation = parse("3d20k1")

starting_gold = Dice(quantity=3, sides=6, multiplier=10)
# OR
starting_gold = parse("3d6*10")

dagger = Dice(sides=4)
# OR
dagger = parse("d4")

elemental_blast = Dice(sides=6, per_level=True)
# OR
elemental_blast = parse("l*d6")

cure_serious_wounds = Dice(quantity=2, sides=8, summand=1)
# OR
cure_serious_wounds = parse("2d8+1")
```

Usage dice can also be defined directly or via `parse`. Defining a `UsageDie`
directly only requires you to input the ordered sequence of dice sides that
comprise the downgrade ladder. There are no restrictions on the dice sequence
you define. Defining one via `parse` restricts you from the space of all
possible `UsageDie`s to a subset that are defined in the *Gold & Gallows*
ruleset. The syntax for parsing usage dice is:

```
[u|z] sides [p prestige]
```

* `u|z`: an indication of whether this `UsageDie` uses the regular downgrade
    ladder or the Zocchi downgrade ladder.
    * `u`: the regular ladder `20 -> 12 -> 10 -> 8 -> 6 -> 4`.
    * `z`: the Zocchi ladder
        `20 -> 16 -> 14 -> 12 -> 10 -> 8 -> 7 -> 6 -> 5 -> 4`.
* `sides`: the number of sides of the first usage die in the chain. It must
    match a value in the chosen ladder or else a `ValueError` is raised.
* `p prestige`: an optional indicator that the usage die restarts at the
    top of the ladder `prestige` number of times after downgrading from
    a d4.


```python
from dice_model import UsageDie, parse

torch = UsageDie(6, 4)
# OR
torch = parse("u6") 

level_4_warlock_daily_spells = UsageDie(7, 6, 5, 4)
# OR
level_4_warlock_daily_spells = parse("z7")

level_8_magic_user_daily_spells = UsageDie(6, 4, 20, 12, 10, 8, 6, 4)
# OR
level_8_magic_user_daily_spells = parse("u6p1")
```

#### Rolling dice and using usage dice

Rolling a `Dice` returns a `RollResult`. The main attr to access is
`RollResult.total` for the outcome of the roll; this can also be accessed
in int contexts.

```python
from dice_model import parse
from dice_roller import roll

starting_gold = parse("3d6*10")
player_inventory = {}

roll_result = roll(starting_gold)

player_inventory["gold"] = roll_result.total
# OR
player_inventory["gold"] = int(roll_result)
```

`RollResult` also carries the attrs `.dice`, `.faces`, and `.kept`, and
property `.face` (an alias for ``.faces[0]`` when `len(faces) == 1`). Normal
use cases will likely ignore these but they are provided for an audit trail
of the roll process.

Using a `UsageDie` via the method `.use()` returns a `UsageResult`. The
main attrs to access are `UsageResult.downgraded` and `UsageResult.exhausted`
to query if the state has changed.

```python
from dice_model import parse

torch = parse("u6")

usage_result = torch.use()

if usage_result.exhausted:
    print("Your torch expires.")
elif usage_result.downgraded:
    print("Your torch flickers; you feel it is one step closer to expiring.")
else:
    print("Your torch continues to burn brightly.")
```

`UsageResult` also carries the audit attrs `.face`, `.sides_before`, and
`.sides_after`. Normal use cases will likely ignore these three and only
reference `.downgraded` and `.exhausted`.

`rng` is an optional parameter to `roll()`. If it is not provided, rolls
will share the package's default implementation, a seedless and hence
nondeterministic `DefaultRng` built from python's random module. Users can
use `DefaultRng` with an optional seed parameter as shown here for
reproducibility, or provide their own `Rng` implementation having a `randint`
method.

```python
from dice_model import parse
from dice_rng import DefaultRng
from dice_roller import roll

dagger = parse("d4")

roll_result = roll(dagger, rng=DefaultRng(seed=12345))

class YourCustomRng:
    def randint(self, low, high):
        ...

roll_result = roll(dagger, rng=YourCustomRng())
```

`level` is another optional parameter to `roll()`. It must be provided if
the `Dice` object has `per_level=True` and is ignored if `per_level=False`.

```python
from dice_model import parse
from dice_roller import roll

elemental_blast = parse("l*d6")
hp = 20

hp -= int(roll(elemental_blast, level=4)) # Rolls 4d6 and subtracts the total.
```

#### Rolling checks and saves

While in general rolling is not ruleset-specific, checks in this project
for the most part are tied to my TTRPG. In *Gold & Gallows*, checks are
attempted by rolling a d20 strictly between a lower and upper bound ("Threading
the Needle"). Unlike some other d20 systems, additive modifiers are not
used. Advantage and disadvantage do exist; they stack and cancel each other
in pairs. Because of this, users of this API will generally want to just
use `roll()` to define their check/save mechanics, unless they want to adopt
the *Gold & Gallows* rules.

```python
from dice_roller import thread_the_needle

enemy_hd = 5
player_attack_value = 15

check_result = thread_the_needle(above=enemy_hd, below=player_attack_value)

if check_result.success:
    print("You hit the monster!")

# The check_result is truthy depending on its success attr, so the following
# also works:

if check_result:
    print("You hit the monster!")
```

The output of `thread_the_needle()` is a `CheckResult` object which in addition
to `.success` also contains the audit attrs `.rolls`, `.lower_bound`,
`.upper_bound`, and `.advantage`.

The `.advantage` attr in `CheckResult` is for auditing the outcome, but
it comes from an optional `advantage` parameter passed into
`thread_the_needle()`. It is represented as an int value, with positive
values representing the amount of advantage stacked, negative values
representing the amount of disadvantage stacked, and defaulting to 0 for
no advantage or disadvantage. Advantage rolls multiple dice and yields a
success if any of the dice meet the bounds; disadvantage rolls multiple
dice and yields a success only when all of the dice meet the bounds.

```python
from dice_roller import thread_the_needle

# Rolls 2 d20s and succeeds if either is 4, 5, or 6:
thread_the_needle(above=3, below=7, advantage=1)

# Rolls 3 d20s and succeeds if all are three are 9:
thread_the_needle(above=8, below=10, advantage=-2)
```

Some *Gold & Gallows* mechanics also require a roll above or below a bound;
these can be handled with `thread_the_needle()` but are also aliased with
`check_above()` and `check_below()`. An optional `tie_succeeds` parameter
(default `False`) modifies whether to include the bound as a success.

```python
from dice_roller import check_above, check_below

check_above(10)
check_below(3, advantage=1)
check_above(17)                     # Success on an 18, 19, or 20.
check_above(17, tie_succeeds=True)  # Success on a 17, 18, 19, or 20.

```

`thread_the_needle()`, `check_above()`, and `check_below()` all can take
an optional rng parameter which is passed into the call to `roll()` inside.

```python
from dice_rng import DefaultRng
from dice_roller import thread_the_needle, check_below

thread_the_needle(above=1, below=10, rng=DefaultRng(1729))

class YourCustomRng:
    def randint(self, low, high):
        ...

check_below(5, rng=YourCustomRng())
```

### Test suite

With dev dependencies installed, run the test suite with `./run_tests.sh`. 
This attempts to optimize which tests run using testmon. To override this, 
use `COVERAGE=1 ./run_tests.sh`.

## Package Layout

### dice_model

`Dice`, `UsageDie`, and `UsageResult` classes. Codecs for parsing string
syntax into dice or usage dice.

### dice_rng

The `Rng` protocol seam with a canonical `DefaultRng` implementation and
a shared `default_rng()` accessor.

### dice_roller

Generic `roll` method and Gold & Gallows-specific `thread_the_needle`,
`check_above`, and `check_below` methods. Returns `RollResult` and
`CheckResult` classes.
