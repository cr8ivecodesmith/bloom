__all__ = [
    'roll',
    'roll_v',
]

import random
import operator as op


def roll(num, sides, mod=0, mod_per_roll=True):
    """Roll dice with symmetric distribution

    :param mod: Modify total based on this number. This can be a positive
        or negative whole number.
    :param type: int

    :param mod: Apply modifier per roll.
    :param type: bool

    """
    total = 0
    for _ in xrange(num):
        rn = random.randint(1, sides)
        if mod_per_roll:
            rn += mod
        total += rn

    if mod_per_roll:
        return total
    else:
        return total + mod


def roll_v(num, sides, high=True, mod=0, mod_per_roll=True):
    """Roll dice with asymmetric distribution

    :param high: Favor higher-than-average if True or lower-than-average
        otherwise.
    :param type: bool

    """
    variance = min
    if not high:
        variance = max

    hand = []
    for _ in xrange(num + 1):
        hand.append(roll(1, sides, mod, mod_per_roll))

    hand.index(variance(hand))
    hand.append(roll(1, sides, mod, mod_per_roll))

    total = reduce(op.add, hand, 0)
    total = total - variance(hand)

    return total
