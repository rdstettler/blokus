import pygame

# Board size and window size
board_size = 21
border_size = 1
square_size = 20
square_size_offside = square_size * 0.5
offside_width = 250
margin = 5
size = (square_size * board_size + 2 * offside_width, square_size * board_size)

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_GRAY = (240, 240, 240)
LIGHT_GRAY_TRANSPARENT = (100, 100, 100, 0.6)
pygame.init()
pygame.font.init()
GAME_FONT = pygame.font.SysFont("Comic Sans MS", 24)
LIGHT_RED = (255, 100, 100)
LIGHT_BLUE = (100, 100, 255)
LIGHT_YELLOW = (255, 255, 100)
LIGHT_GREEN = (100, 255, 100)
PLAYER_COLORS = [RED, GREEN, BLUE, YELLOW]
LIGHT_COLORS = [LIGHT_RED, LIGHT_GREEN, LIGHT_BLUE, LIGHT_YELLOW]

RED_OFFSIDE_START = [0,0]
GREEN_OFFSIDE_START = [0, size[1] / 2]
BLUE_OFFSIDE_START = [offside_width + square_size * board_size, size[1] / 2]
YELLOW_OFFSIDE_START = [offside_width + square_size * board_size, 0]
START_OFFSIDE_POSITIONS = [RED_OFFSIDE_START, GREEN_OFFSIDE_START, BLUE_OFFSIDE_START, YELLOW_OFFSIDE_START]
ALL_PLAYER_STRINGS = ["RED", "GREEN", "BLUE", "YELLOW"]

RED_START = [0,0]
GREEN_START = [0, board_size - 1]
BLUE_START = [board_size - 1, board_size - 1]
YELLOW_START = [board_size - 1, 0]
START_POSITIONS = [RED_START, GREEN_START, BLUE_START, YELLOW_START]

RED_PIECES = []
GREEN_PIECES = []
BLUE_PIECES = []
YELLOW_PIECES = []
ALL_PIECES = [RED_PIECES, GREEN_PIECES, BLUE_PIECES, YELLOW_PIECES]


pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Blokus")

# Set screen background color
screen.fill(GRAY)
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()