__all__ = (
    'GameHud',
    'mask_rows',
)

from e32 import ao_sleep

from pyboom.colors import BLACK, GRAY, WHITE
from pyboom.types import FourPointCoord, TwoPointCoord
from pyboom.utils import enumerate, debug

from bloom.config import OFF_X, OFF_Y, BLOCKS_X, BLOCKS_Y, BLOCK_SIZE
from bloom.config import FPS_LIMIT, SHAPE_DEFS
from bloom.tetromino import draw_block


def mask_rows(buffer, rows):
    x1 = OFF_X
    x2 = x1 + (BLOCKS_X * BLOCK_SIZE)
    coords = FourPointCoord(x1, 0, x2, 0)

    for y in rows:
        coords.y1 = OFF_Y + (y * BLOCK_SIZE)
        coords.y2 = coords.y1 + BLOCK_SIZE
        buffer.rectangle(coords, fill=WHITE)


class GameHud(object):

    def __init__(self, game):
        self.game = game
        self.buffer = game.buffer

        # Initialize border coords
        # Outline
        x1 = OFF_X - 2
        x2 = OFF_X + (BLOCK_SIZE * BLOCKS_X) + 2
        y1 = OFF_Y
        y2 = OFF_Y + (BLOCK_SIZE * BLOCKS_Y) + 2

        self._b1 = FourPointCoord(x1, y1, x1, y2)
        self._b2 = FourPointCoord(x2, y1, x2, y2)
        self._b3 = FourPointCoord(x1, y2, x2, y2)

        # Fill
        self._b4 = FourPointCoord(x1 + 2, y1, x2 - 2, y2 - 2)

        # Initialize stat hud coords
        # Base
        x1 = (
            OFF_X + (BLOCK_SIZE * BLOCKS_X)
            + 2 + BLOCK_SIZE
        )
        x2 = x1 + (BLOCK_SIZE * 4) + 3

        # Score Label
        y1 = 4
        y2 = y1 + BLOCK_SIZE + 2
        self._s1 = FourPointCoord(x1, y1, x2, y2)
        self._s2 = TwoPointCoord(x1 + 5, y2 - 1)

        # Score Value
        y1 = y2 + 2
        y2 = y1 + BLOCK_SIZE + 2
        self._s3 = FourPointCoord(x1, y1, x2, y2)
        self._s4 = TwoPointCoord(x1 + 1, y2 - 1)

        # Level Label
        y1 = y2 + 5
        y2 = y1 + BLOCK_SIZE + 2
        self._s5 = FourPointCoord(x1, y1, x2, y2)
        self._s6 = TwoPointCoord(x1 + 5, y2 - 1)

        # Level Value
        y1 = y2 + 2
        y2 = y1 + BLOCK_SIZE + 2
        self._s7 = FourPointCoord(x1, y1, x2, y2)
        self._s8 = TwoPointCoord(x1 + 16, y2 - 1)

        # Line Label
        y1 = y2 + 5
        y2 = y1 + BLOCK_SIZE + 2
        self._s9 = FourPointCoord(x1, y1, x2, y2)
        self._s10 = TwoPointCoord(x1 + 8, y2 - 1)

        # Line Value
        y1 = y2 + 2
        y2 = y1 + BLOCK_SIZE + 2
        self._s11 = FourPointCoord(x1, y1, x2, y2)
        self._s12 = TwoPointCoord(x1 + 1, y2 - 1)

        # Next piece Label
        y1 = y2 + 10
        y2 = y1 + BLOCK_SIZE + 2
        self._s13 = FourPointCoord(x1, y1, x2, y2)
        self._s14 = TwoPointCoord(x1 + 9, y2 - 1)

        # Next piece Value
        y1 = y2 + 2
        y2 = y1 + BLOCK_SIZE * 3
        self._s15 = FourPointCoord(x1, y1, x2, y2)

        off_y = y1 + 3
        off_x = x1 + 5
        self._s16 = TwoPointCoord(off_y, off_x)
        self.next_shape_key = game.next_shape_key

    def draw(self):
        self.draw_borders()
        self.draw_stats()

    def draw_borders(self):
        buffer = self.buffer

        # Ouline line
        buffer.line(self._b1, width=1, outline=GRAY)
        buffer.line(self._b2, width=1, outline=GRAY)
        buffer.line(self._b3, width=1, outline=GRAY)

        # Board Fill
        buffer.rectangle(self._b4, fill=WHITE, outline=WHITE)

    def draw_stats(self):
        buffer = self.buffer

        # Score
        buffer.rectangle(self._s1, fill=WHITE)
        buffer.text(self._s2, u"SCORE", fill=BLACK)

        buffer.rectangle(self._s3, fill=WHITE)
        score = unicode(self.game.score)
        buffer.text(self._s4, score, fill=BLACK)

        # Level
        buffer.rectangle(self._s5, fill=WHITE)
        buffer.text(self._s6, u"LEVEL", fill=BLACK)

        buffer.rectangle(self._s7, fill=WHITE)
        level = unicode(self.game.level)
        buffer.text(self._s8, level, fill=BLACK)

        # Lines cleared
        buffer.rectangle(self._s9, fill=WHITE)
        buffer.text(self._s10, u"LINES", fill=BLACK)

        buffer.rectangle(self._s11, fill=WHITE)
        lines = unicode(self.game.lines)
        buffer.text(self._s12, lines, fill=BLACK)

        # Next piece
        buffer.rectangle(self._s13, fill=WHITE)
        buffer.text(self._s14, u"NEXT", fill=BLACK)

        buffer.rectangle(self._s15, fill=WHITE)

        shape = SHAPE_DEFS[self.next_shape_key()][0]
        off_y = self._s16[0]
        off_x = self._s16[1]
        for y, row in enumerate(shape):
            for x, val in enumerate(row):
                if val:
                    draw_block(
                        buffer, y, x,
                        size=9, off_y=off_y, off_x=off_x
                    )
