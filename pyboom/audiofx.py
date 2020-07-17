"""
Music and Sound effects

Limitations:
- Only one sound can play at a time
- It's best to stop a sound before playing to avoid RuntimeErrors
- Playing a sound within a handle_event callback causes errors at
  worst, it crashes the app.

"""
__all__ = ('AudioFx',)

from audio import Sound, EOpen
# from pyboom.utils import debug


class AudioFx(object):
    """Audio base class

    """
    _snd = None
    _is_playing = 0

    def _stop(self):
        def func(*args):
            # prev_state = args[0]
            curr_state = args[1]
            if curr_state == EOpen:
                self._snd.stop()
                self._snd.close()
                self._is_playing = 0
        return func

    def play(self, audio_file):
        if self._is_playing:
            return
        try:
            self._is_playing = 1
            self._snd = Sound.open(audio_file)
            if self._snd.state() == EOpen:
                self._snd.stop()  # Avoids runtime errors
                self._snd.play(callback=self._stop())
        except Exception, e:
            # NOTE: Log the error properly
            # debug('[Audio] - %s' % (str(e)), level='error')
            pass
