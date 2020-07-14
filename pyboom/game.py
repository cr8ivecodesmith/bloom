__all__ = ('GameWorld',)

from appuifw import Canvas, EEventKey, EEventKeyUp, app, popup_menu
from e32 import ao_yield, ao_sleep
from graphics import Image
from sysinfo import free_ram, total_ram

from pyboom.colors import BLACK, WHITE
from pyboom.types import SingletonType


FPS_DEFAULT = (1.0 / 60.0)  # ~60FPS
COLOR_MODE = "RGB12"  # 4096 colors @ 12bits/pixel
BG_COLOR = BLACK


class GameWorld(object):
    """Game world class

    """
    __metaclass__ = SingletonType

    def __init__(
        self, title=None, screen_mode=None, fps=None,
        color_mode=None, bg_color=None,
    ):
        app.screen = screen_mode or "full"
        app.title = title or u"PyS60 Game"

        self._game_obj = None
        self._is_running = 0
        if fps is None:
            self.fps = FPS_DEFAULT
        else:
            assert isinstance(fps, int) or isinstance(fps, float)
            self.fps = fps

        self.color_mode = color_mode or COLOR_MODE
        self.bg_color = bg_color or BG_COLOR

        self.canvas = Canvas(
            redraw_callback=self.handle_redraw(),
            event_callback=self.handle_event()
        )
        app.body = self.canvas
        app.exit_key_handler = self.handle_exit()

        self.buffer = Image.new(self.canvas.size, mode=self.color_mode)
        self.buffer.clear(self.bg_color)
        self.handle_redraw()(None)

        self.key_click = None
        self._key_click_release = 1
        self.key_down = None
        self._key_down_release = 1

    def _get_is_running(self): return self._is_running
    def _set_is_running(self, v): self._is_running = v
    is_running = property(_get_is_running, _set_is_running)

    def _get_key_click_release(self): return self._key_click_release
    def _set_key_click_release(self, v): self._key_click_release = v
    key_click_release = property(
        _get_key_click_release, _set_key_click_release)

    def _get_key_down_release(self): return self._key_down_release
    def _set_key_down_release(self, v): self._key_down_release = v
    key_down_release = property(
        _get_key_down_release, _set_key_down_release)

    def _get_game_obj(self): return self._game_obj
    def _set_game_obj(self, v): self._game_obj = v
    game_obj = property(_get_game_obj, _set_game_obj)

    def main(self, game_obj):
        self.game_obj = game_obj

        # Run the game initializer and
        # pass in a reference to to the game world here.
        game_obj.initialize(self)

        # Start the game loop
        assert hasattr(game_obj, 'run'), "Game object needs a run method."
        if not self.is_running:
            self.is_running = 1

        if not hasattr(game_obj, 'handle_timers'):
            game_obj.handle_timers = 0

        handle_timers = game_obj.handle_timers
        run_fn = game_obj.run

        while self.is_running:
            ao_yield()
            run_fn()
            if handle_timers:
                continue
            else:
                ao_sleep(self.fps)

        # Run any termination/cleanup sequence here if any.
        if hasattr(game_obj, 'terminate'):
            game_obj.terminate()

    def show_ram_usage(self):
        x1 = 0
        y1 = 0
        x2 = x1 + 130
        y2 = y1 + 15
        x3 = x1 + 1
        y3 = y1 + 12
        conv = 1024.0

        txt = u"RAM: %.2f / %.2f MB" % (
            (free_ram() / conv / conv),
            (total_ram() / conv / conv)
        )

        self.buffer.rectangle((
            x1, y1, x2, y2
        ), fill=WHITE)
        self.buffer.text((x3, y3), txt, fill=BLACK)

    def handle_exit(self):
        # The game should handle setting the `is_running`
        # flag to 0 from here.
        handled = 0
        handle_exit = None
        if hasattr(self.game_obj, 'handle_exit'):
            handled = 1
            handle_exit = self.game_obj.handle_exit

        def call(*args, **kwargs):
            if handled:
                handle_exit()
            else:
                ans = popup_menu([u"Yes", u"No"], u"Confirm Exit?")
                if ans == 0:
                    self.is_running = 0
        return call

    def handle_redraw(self):
        # Takes as its argument a four-element tuple that contains the
        # top-left and the bottom-right corner of the area
        # that needs to be redrawn.
        has_buffer = hasattr(self, 'buffer')
        has_canvas = hasattr(self, 'canvas')
        if has_canvas and has_buffer:
            buffer = self.buffer
            canvas = self.canvas

            def call(*args, **kwargs):
                rect = args[0]
                canvas.blit(buffer)

            return call

    def handle_event(self):
        def call(*args, **kwargs):
            event = args[0]

            # Sets flags for keypad short clicks (pressed) or holds (down)
            # key releases
            if event["type"] == EEventKey:
                if self.key_down:
                    # It's the second (or more) times we've checked so this
                    # means the user is keeping holding down a button.
                    self.key_down = (event["keycode"], "down")
                    self.key_down_release = 0
                else:
                    self.key_down = (event["keycode"], "pressed")
                    self.key_click_release = 0
            elif event["type"] == EEventKeyUp and self.key_down:
                code, mode = self.key_down
                if mode == "pressed":
                    self.key_click = code
                    self.key_click_release = 1
                if mode == "down":
                    self.key_down_release = 1
                self.key_down = None

            self.game_obj.handle_event(event)

        return call

    def is_key_clicked(self, code):
        if code == self.key_click:
            self.key_click = None
            return 1
        return 0

    def is_key_held(self, code):
        if self.key_down and self.key_down == (code, "down"):
            return 1
        return 0
