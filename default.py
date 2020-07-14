from pyboom.game import GameWorld

from bloom.game import Game
from bloom.config import GAME_TITLE


if __name__ == '__main__':
    import sys

    world = GameWorld(GAME_TITLE)
    world.main(Game())

    sys.exit(0)
