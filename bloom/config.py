"""
Game settings

"""
from os import path

from pyboom.colors import BLACK
from pyboom.colors import CYAN, BLUE, ORANGE, YELLOW, GREEN, MAGENTA, RED

from pyboom.utils import get_project_path


FPS_LIMIT = (1.0 / 60.0)  # 60fps
BG_COLOR = BLACK
GAME_TITLE = u"Bloom"

PROJECT_PATH = get_project_path(GAME_TITLE)
LOG_FILE = path.join(PROJECT_PATH, '%s.log' % (GAME_TITLE.lower()))
if not path.exists(LOG_FILE):
    fh = open(LOG_FILE, 'w')
    fh.write('')
    fh.close()

BLOCK_SIZE = 10

BLOCKS_X = 10
BLOCKS_Y = 40

OFF_Y = BLOCK_SIZE * (BLOCKS_Y / 2) * -1  # Starts offscreen
OFF_X = BLOCK_SIZE * 2

SPAWN_Y = (BLOCKS_Y / 2) - 2  # 2 rows above the visible area
SPAWN_X = 3

# Level FPS modifier from 0-20
LEVEL_SPEED = (
    53, 49, 45, 41, 37, 33, 28, 22, 17, 11,
    10, 9, 8, 7, 6, 6, 5, 5, 4, 4, 3
)
MAX_LEVEL = len(LEVEL_SPEED) - 1
MAX_SCORE = 999999

SCORE_TABLE = (
    # 0 - 1, 2, 3, 4
    (40, 100, 300, 1200),
    # 1 - 1, 2, 3, 4
    (80, 200, 600, 2400),
    # 2 - 1, 2, 3, 4
    (120, 300, 900, 3600),
    # 9 - 1, 2, 3, 4
    (400, 1000, 3000, 12000),
)

FLASH_PRE_DELAY = 0.4
FLASH_POST_DELAY = 0.7

COLOR_IDS = {
    1: CYAN,
    2: BLUE,
    3: ORANGE,
    4: YELLOW,
    5: GREEN,
    6: MAGENTA,
    7: RED,
}
COLOR_DEFS = {
    'I': 1,
    'J': 2,
    'L': 3,
    'O': 4,
    'S': 5,
    'T': 6,
    'Z': 7,
}
SHAPE_KEYS = ('I', 'J', 'L', 'O', 'S', 'T', 'Z')
SHAPE_DEFS = {
    'I': (
        ((0, 0, 0, 0),
         (1, 1, 1, 1),
         (0, 0, 0, 0),
         (0, 0, 0, 0)),
        ((0, 0, 1, 0),
         (0, 0, 1, 0),
         (0, 0, 1, 0),
         (0, 0, 1, 0)),
        ((0, 0, 0, 0),
         (0, 0, 0, 0),
         (1, 1, 1, 1),
         (0, 0, 0, 0)),
        ((0, 1, 0, 0),
         (0, 1, 0, 0),
         (0, 1, 0, 0),
         (0, 1, 0, 0)),
    ),
    'J': (
        ((2, 0, 0),
         (2, 2, 2),
         (0, 0, 0)),
        ((0, 2, 2),
         (0, 2, 0),
         (0, 2, 0)),
        ((0, 0, 0),
         (2, 2, 2),
         (0, 0, 2)),
        ((0, 2, 0),
         (0, 2, 0),
         (2, 2, 0)),
    ),
    'L': (
        ((0, 0, 3),
         (3, 3, 3),
         (0, 0, 0)),
        ((0, 3, 0),
         (0, 3, 0),
         (0, 3, 3)),
        ((0, 0, 0),
         (3, 3, 3),
         (3, 0, 0)),
        ((3, 3, 0),
         (0, 3, 0),
         (0, 3, 0)),
    ),
    'O': (
        ((0, 4, 4, 0),
         (0, 4, 4, 0),
         (0, 0, 0, 0)),
    ),
    'S': (
        ((0, 5, 5),
         (5, 5, 0),
         (0, 0, 0)),
        ((0, 5, 0),
         (0, 5, 5),
         (0, 0, 5)),
        ((0, 0, 0),
         (0, 5, 5),
         (5, 5, 0)),
        ((5, 0, 0),
         (5, 5, 0),
         (0, 5, 0)),
    ),
    'T': (
        ((0, 6, 0),
         (6, 6, 6),
         (0, 0, 0)),
        ((0, 6, 0),
         (0, 6, 6),
         (0, 6, 0)),
        ((0, 0, 0),
         (6, 6, 6),
         (0, 6, 0)),
        ((0, 6, 0),
         (6, 6, 0),
         (0, 6, 0)),
    ),
    'Z': (
        ((7, 7, 0),
         (0, 7, 7),
         (0, 0, 0)),
        ((0, 0, 7),
         (0, 7, 7),
         (0, 7, 0)),
        ((0, 0, 0),
         (7, 7, 0),
         (0, 7, 7)),
        ((0, 7, 0),
         (7, 7, 0),
         (7, 0, 0)),
    ),
}
