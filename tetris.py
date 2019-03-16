import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30
#still do not understand these dimensions
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# SHAPE FORMATS

S = [['.....',
    '......',
    '..00..',
    '.00...',
    '.....'],
    ['.....',
    '..0..',
    '..00.',
    '...0.',
    '.....']]

Z = [['.....',
    '.....',
    '.00..',
    '..00.',
    '.....'],
    ['.....',
    '..0..',
    '.00..',
    '.0...',
    '.....']]

I = [['..0..',
    '..0..',
    '..0..',
    '..0..',
    '.....'],
    ['.....',
    '0000.',
    '.....',
    '.....',
    '.....']]

O = [['.....',
    '.....',
    '.00..',
    '.00..',
    '.....']]

J = [['.....',
    '.0...',
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '..00.',
    '..0..',
    '..0..',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '...0.',
    '.....'],
    ['.....',
    '..0..',
    '..0..',
    '.00..',
    '.....']]

L = [['.....',
    '...0.',
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '..0..',
    '..0..',
    '..00.',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '.0...',
    '.....'],
    ['.....',
    '.00..',
    '..0..',
    '..0..',
    '.....']]

T = [['.....',
    '..0..',
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '..0..',
    '..00.',
    '..0..',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '..0..',
    '.....'],
    ['.....',
    '..0..',
    '.00..',
    '..0..',
    '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0 #press up arrow to add and change rotation

def create_grid(locked_position = {}):
    grid = [[(0,0,0)for x in range(10)] for x in range(20)] #default to black
    #above is the raw, blank grid. Below, putting in the locked pieces
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_position: #the dictionary passed in
                c = locked_position[(j,i)]#dictionary value for that key into "c".
                grid[i][j] = c#the grid at (x,y) gets changed to that value (the color)
    return grid

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    # below: to add all of the x and y coordinates as the shape falls, in addition to the rows (i) and columns (j)
    for i, line in enumerate(format):#to search for a 0 or period.
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
        # this could be because spawning happens above play field.

    return positions

def valid_space(shape, grid):
    accepted_pos = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)] #accepted only if empty (0,0,0)
    accepted_pos = [j for sub in accepted_pos for j in sub] #overwrites the above

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1: #only worried about active field of play
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x,y = pos #splitting the tuple
        if y < 1:
            return True
    return False #if every position is greater than 1, we haven't lost yet.

def get_shape(): #no arugment passed? Odd.
    return Piece(5, 0, random.choice(shapes))
    # randomizes the shape we see falling down, using class Pieces, which takes in the three arguments.
    # the screen. Notice there is no argument for the outer function.

def draw_text_middle(text, size, color, surface):
    pass

def draw_grid(surface, grid): #"surface" hosts images in pygame; grid from create_grid
    sx = top_left_x
    sy = top_left_y
    # below: to superimpose the visible lines over the grid
    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128),(sx, sy + i*block_size),(sx + play_width, sy)) 
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))

def clear_rows(grid, locked):
    inc = 0 #inc = increment
    for i in range(len(grid) - 1, - 1, - 1): #loops through the grid backwards
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1 #counts the number of rows deleted to be accounted for.
            ind = i #ind = index; need to track it becuase of how rows will shift.
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x [1]) [::-1]:
            x,y = key
            if y < ind:
                newKey = (x,y + inc)
                locked[newKey] = locked.pop(key)

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 0:
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)
                #above, our goal is to draw a static image; unconcerned about how it moves.

    surface.blit(label, (sx + 10, sy - 30))

def draw_window(surface, grid):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))  # anti-aliasing of 1

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 30))
    # above: middle of screen - width of label; the y can be static
    
    for i in range(len(grid)):  # to draw the objects on to the screen
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size,
                                                   top_left_y + i*block_size, block_size, block_size), 0)
            #above: last two are width and height. block_size is 30 in all cases. Last is a fill, so it isn't just a border.
    # below: to draw the red box
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x,top_left_y, play_width, play_height), 4)

    draw_grid(surface,grid)

def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27

    while run:
        grid = create_grid(locked_positions) #grid needs constant updating
        fall_time += clock.get_rawtime() #rawtime gets the time since the last tick.
        clock.tick()

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1 # automatically moves piece down         
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1  # +1 to pretend the move never happened.
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP: #rotation could cause border violations
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece) #to determine if it is on the ground
        #below: adds the colors to the grid                                                #or otherwise needs to be locked.
        for i in range(len(shape_pos)):
            x,y = shape_pos[i] #current iteration
            if y > -1: #means we're not above the screen
                grid[y][x] = current_piece.color #places the color on the grid

        if change_piece: #think of this just as a boolean condition, not a function
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color #a dictionary {(x,y):(255,255,255)}
            current_piece = next_piece #in variables at top of main()
            next_piece = get_shape()   #in variables at top of main()
            change_piece = False #b/c a new piece will spawn at the top

            draw_window(win, grid)
            draw_next_shape(next_piece, win)
            pygame.display.update()

        if check_lost(locked_positions):
            run = False
    pygame.display.quit()


def main_menu(win):
    main(win)
#below: closes previous display
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu(win)  # start game
