import pygame

pygame.mixer.pre_init(44100, -16, 1, 1)
pygame.mixer.init()

pygame.init()

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
GRAY  = (20, 20, 20)
BLUE  = (0, 0, 200)
RED   = (200, 0, 0)

# SCREEN CONFIGURATIONS
SCREEN_WIDTH    = 1000
SCREEN_HEIGHT   = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BG_COLOR = BLACK

# CLOCK CONFIGURATIONS
clock = pygame.time.Clock()
FPS = 60

# GAME CONTROL VARIABLES
game_over = False
pause = False
new_game = True
round_finished = False
win = False
MAX_POINTS = 10

# GAME MODE
leftLevel = 'normal'
level = 'ultimate'   # the game difficulty
logic = 'simple' # for ball


# BOARD CONFIGS
BOARD_WIDTH     = 10
BOARD_HEIGHT    = 100
BOARD_SPEED     = 5
BOARD_COLOR     = WHITE


# BALL CONFIGS
BALL_RADIUS     = 5
BALL_SPEED      = 5
BALL_COLOR      = GREEN


# LINE & CIRCLE CONFIGS
DRAW_LINE       = True
LINE_COLOR      = WHITE
LINE_WIDTH      = 1

DRAW_CIRCLE     = True
CIRCLE_COLOR    = WHITE
CIRCLE_WIDTH    = 3
CIRCLE_RADIUS   = 50


# FONTS
FONT_SIZE   = 40
FONT_COLOR  = WHITE
font = pygame.font.SysFont('Futura', size=FONT_SIZE)

# SOUNDS
PLAY_SOUND  = True
collide_sound = pygame.mixer.Sound('audio/ball.ogg')
collide_sound.set_volume(1)


# BUTTONS
BUTTON_TEXT_COLOR   = WHITE
BUTTON_BG_COLOR     = BLACK
BUTTON_WIDTH        = 150
BUTTON_HEIGHT       = 50
BUTTON_BORDER_COLOR = (0, 200, 0)
BUTTON_BORDER       = 3

# MENU
MENU_BG_COLOR       = GRAY
menu                = None
mainMenu            = None
settingsMenu        = None

# AI
USE_AI              = True