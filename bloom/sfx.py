__all__ = ('Sfx',)

from os import path

from pyboom.audiofx import AudioFx
from bloom.config import SFX_PATH


class Sfx(AudioFx):

    def __init__(self):
        self._move = path.join(SFX_PATH, 'move.wav')
        self._rotate = path.join(SFX_PATH, 'rotate.wav')
        self._land = path.join(SFX_PATH, 'land.wav')
        self._clear_rows = path.join(SFX_PATH, 'clear_rows.wav')

    def move(self):
        self.play(self._move)
        return

    def rotate(self):
        self.play(self._rotate)
        return

    def land(self):
        self.play(self._land)
        return

    def clear_rows(self):
        self.play(self._clear_rows)
        return
