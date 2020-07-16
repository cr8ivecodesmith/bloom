__all__ = [
    'any',
    'all',
    'enumerate',
]
from __future__ import generators

import time
from os import path


DRIVE_C = 'c:\\'
DRIVE_E = 'e:\\'
SYSTEM_APPS = 'system\\apps\\'


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


def get_project_path(project_name):
    """Get path where the project is installed

    """
    loc = '%s%s%s' % (DRIVE_E, SYSTEM_APPS, project_name)
    if path.exists(loc):
        return loc

    loc = '%s%s%s' % (DRIVE_C, SYSTEM_APPS, project_name)
    if path.exists(loc):
        return loc

    return


def debug(msg, level=None, log_file=None):
    """Prints a debug message

    """
    if isinstance(level, str):
        level = level.upper()
    else:
        level = 'DEBUG'
    tpl = u"[%s] %s - %s\n" % (
        time.strftime("%Y-%m-%d %H:%M:%S"), level, str(msg)
    )
    if log_file and path.exists(log_file):
        fh = open(log_file, 'a')
        print >> fh, tpl
        fh.close()
    else:
        print tpl
