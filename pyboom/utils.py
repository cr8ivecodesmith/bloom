__all__ = [
    'any',
    'all',
    'enumerate',
]
from __future__ import generators
import time


def any(seq):
    """Returns 1 if at least 1 item in the sequence is truthy.

    """
    for i in seq:
        if i:
            return 1
    return 0


def all(seq):
    """Returns 1 if all items in the sequence is truthy.

    """
    for i in seq:
        if not i:
            return 0
    return 1


def enumerate(seq, reverse=0):
    """Generates the sequence item with its index.

    """
    ids = None
    if reverse:
        ids = xrange(len(seq) - 1, -1, -1)
    else:
        ids = xrange(len(seq))
    for i in ids:
        yield i, seq[i]


def debug(msg):
    """Prints a debug message

    """
    tpl = u"[%s] DEBUG - %s\n" % (
        time.strftime("%Y-%m-%d %H:%M:%S"), str(msg)
    )
    print tpl
