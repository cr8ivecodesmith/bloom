"""
Data Types

"""
import thread


class SingletonType(type):
    """Thread-safe Singleton Type Metaclass

    Usage:

    class ClassName(object):
        __metaclass__ = SingletonType

    """
    _instances = {}
    _lock = thread.allocate_lock()

    def __call__(cls, *args, **kwargs):
        if not cls._lock.locked():
            if cls not in cls._instances:
                instance = super(SingletonType, cls).__call__(*args, **kwargs)
                cls._instances[cls] = instance
                cls._lock.acquire()
        return cls._instances[cls]

    def __del__(cls):
        if cls._lock.locked():
            cls._lock.release()


class FourPointCoord(object):
    __slots__ = ('x1', 'y1', 'x2', 'y2',)

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __getitem__(self, i):
        _coord = (self.x1, self.y1, self.x2, self.y2)
        return _coord[i]

    def __len__(self):
        return 4

    def __repr__(self):
        return "<FourPointCoord (%d, %d, %d, %d)>" % (
            self.x1, self.y1, self.x2, self.y2
        )


class TwoPointCoord(object):
    __slots__ = ('x', 'y',)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, i):
        _coord = (self.x, self.y)
        return _coord[i]

    def __len__(self):
        return 2

    def __repr__(self):
        return "<TwoPointCoord (%d, %d)>" % (
            self.x, self.y
        )
