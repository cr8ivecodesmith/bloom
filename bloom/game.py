__all__ = ('Game',)

from appuifw import popup_menu
from e32 import ao_sleep
from key_codes import EKeyLeftArrow, EKeyRightArrow, EKeyUpArrow, EKeyDownArrow
from key_codes import EKey5, EKey7

from pyboom.utils import debug

from bloom.ui import GameHud, mask_rows
from bloom.board import Board
from bloom.tetromino import Tetromino
from bloom.config import FLASH_PRE_DELAY, FLASH_POST_DELAY
from bloom.config import FPS_LIMIT, LEVEL_SPEED, MAX_LEVEL
from bloom.config import SCORE_TABLE, MAX_SCORE
from bloom.config import LOG_FILE
from bloom.sfx import Sfx


class Game(object):

    def initialize(self, world):
        # Runs before the game loop starts
        self.world = world

        self.buffer = world.buffer
        self.buffer_clear = world.buffer.clear

        self.canvas = world.canvas
        self.canvas_blit = world.canvas.blit

        self.bg_color = world.bg_color
        self.is_key_clicked = world.is_key_clicked
        self.is_key_held = world.is_key_held

        # Set to true if you want to handle game timers yourself
        self.handle_timers = 1

        # Initialize the game board
        self.board = Board(self.buffer)
        self.board_draw = self.board.draw
        self.flush_shape = self.board.flush_shape
        self.clear_win_rows = self.board.clear_win_rows
        self.get_win_rows = self.board.get_win_rows
        self.is_filled = self.board.is_filled

        # Initialize the Tetromino handler
        self.tetromino = Tetromino(self.buffer, self.board)
        self.tetromino_draw = self.tetromino.draw
        self.tetromino_move = self.tetromino.move
        self.tetromino_rotate = self.tetromino.rotate

        # Stat trackers
        self.start_level = self.get_start_level()
        self.score = 0
        self.lines = 0
        self.level = self.start_level
        self.soft_drops = 0
        self.level_speed = FPS_LIMIT * LEVEL_SPEED[self.level]
        self.next_shape_key = self.tetromino.check_next_shape_key
        self.win_rows = None

        # Initialize HUD
        game_hud = GameHud(self)
        self.draw_game_hud = game_hud.draw

        # Sound effects
        try:
            self.sfx = Sfx()
        except Exception, e:
            debug(
                '[Game] - Sfx - %s' % (str(e)),
                level='ERROR', log_file=LOG_FILE
            )
            raise

        # Flags for sfx assoc
        self.sfx_move = 0
        self.sfx_rotate = 0
        self.sfx_land = 0
        self.sfx_clear_rows = 0

        self.redraw()

    def terminate(self):
        # Runs after the game loop when the world.is_running flag
        # Has been set to false
        return

    def update_score(self, win_rows_count):
        if self.score > MAX_SCORE:
            return

        y = self.level
        if 3 <= self.level < 9:
            y = 2
        elif self.level >= 9:
            y = 3

        x = win_rows_count - 1
        if win_rows_count > 3:
            x = 3
        self.score += SCORE_TABLE[y][x]
        if self.soft_drops:
            self.score += SCORE_TABLE[0][x] * (self.soft_drops + 1)
            self.soft_drops = 0

    def update_level(self, win_rows_count):
        self.lines += win_rows_count
        if self.level == self.start_level:
            if ((self.start_level * 10) + 10) == self.lines:
                self.level += 1
                self.level_speed = FPS_LIMIT * LEVEL_SPEED[self.level]
        elif self.start_level < self.level <= MAX_LEVEL:
            if self.lines % 10.0 == 0:
                self.level += 1
                self.level_speed = FPS_LIMIT * LEVEL_SPEED[self.level]

    def flash_win_rows(self):
        if self.win_rows:
            mask_rows(self.buffer, self.win_rows)

    def run(self):
        self.redraw()

        # Move this out on it's own function
        if self.tetromino.is_landed():
            self.flush_shape(self.tetromino.shape)
            self.tetromino.next_shape()

            self.win_rows = list(self.get_win_rows())
            if self.win_rows:
                win_rows_count = len(self.win_rows)
                self.sfx_clear_rows = 1

                # On
                self.redraw(win_anim_fn=self.flash_win_rows)
                ao_sleep(FLASH_PRE_DELAY)
                # Off
                self.redraw()
                ao_sleep(FLASH_POST_DELAY)

                self.update_score(win_rows_count)
                self.clear_win_rows()
                self.update_level(win_rows_count)
                self.win_rows = None

                ao_sleep(FLASH_POST_DELAY)

            self.soft_drops = 0
            self.sfx_land = 1
            self.redraw()

            if self.is_filled():
                self.check_restart()

            ao_sleep(FPS_LIMIT)

        self.auto_move()

    def check_restart(self):
        ans = popup_menu([u"Yes", u"No"], u"Play again?")
        if ans == 0:
            self.board.clear()
            self.start_level = self.get_start_level()
            self.score = 0
            self.lines = 0
            self.level = self.start_level
            self.soft_drops = 0
            self.level_speed = FPS_LIMIT * LEVEL_SPEED[self.level]
        else:
            self.world.is_running = 0

    def auto_move(self):
        ao_sleep(self.level_speed)
        self.tetromino_move(1, 0)
        self.redraw()

    def get_start_level(self):
        choices = u"0 1 2 3 4 5 6 7 8 9".split()
        ans = popup_menu(choices, u"Choose level")
        return ans

    def handle_event(self, event):
        is_key_clicked = self.is_key_clicked
        is_key_held = self.is_key_held

        # Movement
        if is_key_clicked(EKeyLeftArrow) or is_key_held(EKeyLeftArrow):
            self.tetromino_move(0, -1)
            self.sfx_move = 1
        elif is_key_clicked(EKeyRightArrow) or is_key_held(EKeyRightArrow):
            self.tetromino_move(0, 1)
            self.sfx_move = 1

        # Soft drops
        elif is_key_clicked(EKeyDownArrow) or is_key_held(EKeyDownArrow):
            self.tetromino_move(1, 0)
            self.soft_drops += 1
            self.sfx_move = 1

        # Rotation
        elif is_key_clicked(EKeyUpArrow) or is_key_clicked(EKey5):
            self.tetromino_rotate(1)
            self.sfx_rotate = 1
        elif is_key_clicked(EKey7):
            self.sfx_rotate = 1
            self.tetromino_rotate(-1)

        self.redraw(is_event=1)

    def redraw(self, win_anim_fn=None, is_event=None):
        self.buffer_clear(self.bg_color)

        self.draw_game_hud()
        self.board_draw()
        self.tetromino_draw()

        # Determine which sfx to play
        if not is_event:
            if self.sfx_move:
                self.sfx.move()
                self.sfx_move = 0
            elif self.sfx_rotate:
                self.sfx.rotate()
                self.sfx_rotate = 0

            if self.sfx_land:
                self.sfx.land()
                self.sfx_land = 0
            if self.sfx_clear_rows:
                self.sfx.clear_rows()
                self.sfx_clear_rows = 0

        # Flash win row animation
        if win_anim_fn:
            win_anim_fn()

        # self.world.show_ram_usage()
        self.canvas_blit(self.buffer)
