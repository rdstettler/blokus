import pygame
import sys
import game
import constants as c


# Define player pieces_shapes as collection of arrays
pieces_shapes = (
    [[0,0]],
    [[0,0],[0,1]],
    [[0,0],[0,1],[0,2]],
    [[0,0],[0,1],[0,2],[0,3]],
    [[0,0],[0,1],[0,2],[0,3],[0,4]],
    [[0,0],[0,1],[1,0]], # small L
    [[0,0],[0,1],[0,2],[1,0]], # L
    [[0,0],[1,0],[0,1],[1,1]], # Square
    [[0,0],[1,0],[1,1],[2,1]], # S-piece
    [[0,0],[1,0],[2,0],[1,1]], # small T-piece
    [[0,0],[0,1],[0,2],[0,3],[1,0]], # big L
    [[0,0],[1,0],[0,1],[1,1],[0,2]], # Square with nibble
    
    [[0,0],[1,0],[2,0],[1,1],[1,2]], # T-piece
    [[0,0],[1,0],[1,1],[1,2],[2,2]], # Z-piece
    [[0,0],[1,0],[0,1],[0,2],[1,2]], # C-piece
    [[0,0],[1,1],[1,0],[2,0],[3,0]], # F-piece
    [[0,0],[1,0],[1,1],[2,1],[2,2]], # W-piece
    [[0,0],[1,0],[1,1],[1,2],[2,1]],
    [[0,0],[1,0],[-1,0],[0,1],[0,-1]], # X-Piece
    [[0,0],[1,0],[2,0],[0,1],[0,2]], # Corner Piece
    [[0,0],[1,0],[1,1],[2,1],[3,1]]
)

class Button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(c.screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
        pygame.draw.rect(c.screen, self.color, (self.x,self.y,self.width,self.height),0)
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 10)
            text = font.render(self.text, 1, (0,0,0))
            c.screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


AUTO_PLAY = True
PREVIEW_TILES = True
pyticks = 10000

any_piece_selected = False
# add button that triggers computer to play
button = Button(c.LIGHT_GRAY, c.SCREEN_WIDTH - 100, c.SCREEN_HEIGHT - 30, 90, 30, "Computer")
button.draw()
GAME = game.Game(pieces_shapes)
running = True
while running:
    for event in pygame.event.get():
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        GAME.mouse_event(pygame.mouse.get_pos(), event)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and button.isOver([mouse_x, mouse_y]):
            GAME.cpu_placement()
    
    if PREVIEW_TILES:
        GAME.board.trigger_allowed_tiles()

    if AUTO_PLAY:
        if pyticks > pygame.time.get_ticks():
            GAME.cpu_placement()
            pyticks = pygame.time.get_ticks() + 1000
    GAME.drawing()
    
    # Add colored Circle at the bottom left of the screen indicating the current player
    pygame.draw.circle(c.screen, GAME.current_player_color(), (c.square_size_offside, c.size[1] - c.square_size_offside), c.square_size_offside)
    
    # Aktualisiere das Display
    pygame.display.flip()

# Beende das Programm
pygame.quit()
sys.exit()
