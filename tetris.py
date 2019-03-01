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

# GLOBALS VARS: good practice to put the global variables up front.
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2 #still not sure what these lines are describing.
top_left_y = s_height - play_height

# SHAPE FORMATS: every configuration each shape can assume on the screen 
# note: need to give each shape a buffer of at least one grid square.
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

shapes = [S, Z, I, O, J, L, T] #grid-defined above, the shapes are put into a list.
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape

# There's clearly going to be some appreciable overlap with the blackjack game, in terms of governing the filling of spaces.

class Piece(object): #like the blackjack game, the largest coherent concept becomes an object
	def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]  #this is the index method, which returns the index of the 
                                                        #argument(in this case 'shape') provided. This in turn 
                                                        #becomes the index provided to shape_colors. (Ultimately)
                                                        #shape and shape_colors are linked by a common index position
        self.rotation = 0   # default of 0, so just clicking up
                            # arrow rotates among the shape options

def create_grid(locked_positions={}): #locked_pos will be a dictionary
	grid = [[(0,0,0) for x in range (10)] for x in range (20)] #works as an embedded for loop: one list of 10 for ever row (20)
    #Note that (0,0,0) is black, which will serve as a defualt
    for i in range(len(grid)): #the embedding is apparent here.
        for j in range(len(grid[i])): #whichever of those 1-20 you are in.
            if (j,i) in locked_pos: #note that j is x value and i is y value
                c = locked_pos[(j,i)] #determining that it's locked as x and y coordinates
                grid[i][j] = c #translating that to the two for loops

def convert_shape_format(shape):
	pass

def valid_space(shape, grid):
	pass

def check_lost(positions):
	pass

def get_shape():
	pass


def draw_text_middle(text, size, color, surface):
	pass

def draw_grid(surface, row, col):
	pass

def clear_rows(grid, locked):
    pass

def draw_next_shape(shape, surface):
    pass

def draw_window(surface):
	pass

def main():
	pass

def main_menu():
	pass

main_menu()  # start game