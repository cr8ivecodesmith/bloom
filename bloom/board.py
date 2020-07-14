__all__ = (
    'Board',
)
from __future__ import generators

from pyboom.types import SingletonType
from pyboom.utils import enumerate, all, any

from bloom.config import BLOCKS_Y, BLOCKS_X, OFF_Y, OFF_X
from bloom.tetromino import draw_block


class Board(object):

    __slots__ = (
       'buffer', 'size', '_board', 'clear', 'draw',
        'get_win_rows', 'clear_win_rows',
        'flush_shape', 'fill_point',
    )

    def __init__(self, buffer):
        self.size = (BLOCKS_Y, BLOCKS_X)
        self.buffer = buffer
        self._board = None
        self.clear()
        self.fill_point = BLOCKS_Y // 2 - 1

    def clear(self):
        self._board = [
            [None] * self.size[1] for _ in xrange(self.size[0])
        ]

    def draw(self):
        board = self._board
        buffer = self.buffer
        draw = draw_block
        off_x = OFF_X
        off_y = OFF_Y
        for y, row in enumerate(board):
            for x, val in enumerate(row):
                if val:
                    draw(
                        buffer, y, x, color=val,
                        off_y=off_y, off_x=off_x
                    )

    def flush_shape(self, shape):
        board = self._board
        for val, y, x in shape.get_board_pos():
            board[y][x] = val

    def get_win_rows(self):
        board = self._board
        for y, row in enumerate(board):
            if all(row):
                yield y

    def clear_win_rows(self):
        board = self._board
        size_x = self.size[1]
        for y in self.get_win_rows():
            board[y] = [None] * size_x
            for i in xrange(y, 0, -1):
                j = i - 1
                board[j], board[i] = board[i], board[j]

    def is_filled(self):
        if any(self._board[self.fill_point]):
            return 1
        return 0

    def __getitem__(self, i):
        return self._board[i]

    def __len__(self):
        return self.size

    def __repr__(self):
        return "<Board (%d, %d)>" % self.size
