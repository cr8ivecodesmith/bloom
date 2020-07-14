__all__ = (
    'Tetromino',
    'draw_block',
)
from __future__ import generators
from random import shuffle

from pyboom.colors import BLACK, WHITE
from pyboom.types import SingletonType
from pyboom.utils import enumerate, any, all, debug

from bloom.config import BLOCK_SIZE, BLOCKS_Y, BLOCKS_X, OFF_Y, OFF_X
from bloom.config import SPAWN_Y, SPAWN_X
from bloom.config import COLOR_IDS, SHAPE_DEFS, SHAPE_KEYS


def draw_block(
    buffer, row, col, size=None, color=None, off_y=0, off_x=0
):
    size = size or BLOCK_SIZE
    py = off_y + (size * row)
    px = off_x + (size * col)

    if isinstance(color, int):
        color = COLOR_IDS[color]
    else:
        color = color or BLACK
    outline = WHITE

    buffer.rectangle((
        px, py, px + size, py + size
    ), outline=WHITE)
    buffer.rectangle((
        px + 1, py + 1, px + (size - 1), py + (size - 1)
    ), fill=color)


class Tetromino(object):
    """Tetromino

    - Generate a new tetromino
    - Manage movement
    - Manage rotation
    - Check collisions with game boarders
    - Check collisions with landed blocks
    - Check landing status
    - Check next shape for status HUD

    """
    def __init__(self, buffer, board):
        self.buffer = buffer
        self.board = board

        self._shape_id = 0
        self._shape_id_max = len(SHAPE_KEYS) - 1
        self._shape_keys = list(SHAPE_KEYS)
        shuffle(self._shape_keys)

        self.shape = self.init_shape(self._next_shape_key())

    def init_shape(self, shape_key):
        return Shape(SHAPE_DEFS[shape_key], self, SPAWN_Y, SPAWN_X)

    def _next_valid_shape_key(self):
        i = self._shape_id + 1
        if i > self._shape_id_max:
            i = 0
        return i

    def _next_shape_key(self):
        shape_key = self._shape_keys[self._shape_id]
        i = self._shape_id + 1
        if i > self._shape_id_max:
            i = 0
            shuffle(self._shape_keys)
        self._shape_id = i
        return shape_key

    def next_shape(self):
        self.shape = self.init_shape(self._next_shape_key())

    def check_next_shape_key(self):
        return self._shape_keys[self._shape_id]

    def draw(self):
        self.shape.draw()

    def _check_yx(self, y, x, row=0, col=0):
        y += row
        x += col
        sides = x >= 0 and x <= (BLOCKS_X - 1)
        bottom = y <= (BLOCKS_Y - 1)
        if y >= 0 and bottom and sides:
            if not self.board[y][x]:
                return 1
        elif sides and bottom:
            return 1
        return 0

    def validate_row_move(self, row):
        if row == 0:
            return 0
        check_yx = self._check_yx
        valid = all([
            check_yx(y, x, row=row) for v, y, x in self.shape.get_board_pos()
        ])
        if valid:
            return 1
        return 0

    def validate_col_move(self, col):
        if col == 0:
            return 0
        check_yx = self._check_yx
        valid = all([
            check_yx(y, x, col=col) for v, y, x in self.shape.get_board_pos()
        ])
        if valid:
            return 1
        return 0

    def validate_rotation(self, direction):
        next_id = self.shape.get_next_shape_id(direction)
        new_shape = self.shape.shape_defs[next_id]
        check_yx = self._check_yx

        valid = all([
            check_yx(y, x) for v, y, x in self.shape.get_board_pos(new_shape)
        ])
        if valid:
            return 1
        return 0

    def move(self, row, col):
        if self.validate_row_move(row):
            self.shape.row += row
        if self.validate_col_move(col):
            self.shape.col += col

    def rotate(self, direction):
        if self.validate_rotation(direction):
            self.shape.idx = direction

    def is_landed(self):
        board = self.board
        def is_valid(v, y, x):
            bottom = y == (BLOCKS_Y - 1)
            by = y + 1
            if by > (BLOCKS_Y - 1):  # Will exceed the bottom border
                by = y
            if bottom or board[by][x]:
                return 1
            return 0
        valid = any([
            is_valid(v, y, x) for v, y, x in self.shape.get_board_pos()
        ])
        if valid:
            return 1
        return 0


class Shape(object):
    """Tetromino Shape

    - Keep track of blocks position relative to the board
    - Manage drawing on board
    - Peek at next shape for rotation checks

    """
    __slots__ = (
        'shape_defs', 'tetromino', 'current', '_idx',
        'row', 'col',
        'buffer', 'get_board_pos', 'draw',
        'get_next_shape_id',
    )

    def __init__(
        self, shape_defs, tetromino, row, col
    ):
        self.tetromino = tetromino
        self.shape_defs = shape_defs
        self.buffer = tetromino.buffer

        self._idx = 0

        # This is the topleft pos of the shape in the board
        self.row = row
        self.col = col

    def _get_current(self): return self.shape_defs[self.idx]
    current = property(_get_current)

    def _get_idx(self): return self._idx
    def _set_idx(self, val):
        self._idx = self.get_next_shape_id(val)
    idx = property(_get_idx, _set_idx)

    def get_next_shape_id(self, direction):
        # direction is either 1, -1 or 0
        assert 1 >= direction >= -1
        i = self._idx + direction
        max = len(self.shape_defs) - 1
        if i < 0:
            i = max
        elif i > max:
            i = 0
        return i

    def get_board_pos(self, shape=None):
        # Get the position of each valid block on the board
        sy = self.row
        sx = self.col
        shape = shape or self.current
        for y, row in enumerate(shape):
            for x, val in enumerate(row):
                if val:
                    yield val, y + sy, x + sx

    def draw(self):
        # Draw shape on the board
        off_y = OFF_Y
        off_x = OFF_X
        buffer = self.buffer
        for val, y, x in self.get_board_pos():
            draw_block(buffer, y, x, color=val, off_y=off_y, off_x=off_x)
