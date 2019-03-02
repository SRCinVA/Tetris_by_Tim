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
		self.rotation = 0 # default of 0, so just clicking up
						# arrow rotates among the shape options

def create_grid(locked_positions={}): #locked_pos will be a passed-in dictionary
	grid = [[(0,0,0) for x in range (10)] for x in range (20)] #works as an embedded for loop: one list of 10 for ever row (20)
																#Note that (0,0,0) is black, which will serve as a defualt.
	# this for loop's job is to apply the position and color of the bricks that have already been locked down.
	for i in range(len(grid)): #the embedding is apparent in the embedded for loops.
		for j in range(len(grid[i])): #whichever of those 1-20 you are in.
			if (j,i) in locked_pos: #note that j is x value and i is y value
				c = locked_pos[(j,i)] #determining the x and y coordinates of what is locked and passing in those keys from the dictionary.
				grid[i][j] = c #finally, translating that locked cell to indexes related to the for loops. [i] was the outer for loop.
	return grid # "returned to whereer we're calling it from". Hopefully that is answered.

def convert_shape_format(shape):
	pass

def valid_space(shape, grid):
	pass

def check_lost(positions):
	pass

def get_shape():
	return Piece(5,0,random.choice(shapes))  #randomizes the shape we see falling down, using class Pieces, which takes in the three arguments.
									# the screen. Notice there is no
									# argument for the outer function.

def draw_text_middle(text, size, color, surface):
	pass

def draw_grid(surface, grid):
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			pygame.graw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y+ i*block_size, block_size, block_size),0)
	# the point here is to loop through every color on the grid and apply it to the surface.
	# the 0 is to fill in the shape and not just draw a border for it. Why...???

	#for the red area delimiting the play area:
	pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 4)

def clear_rows(grid, locked):
	pass

def draw_next_shape(shape, surface):
	pass

def draw_window(surface, grid):
	surface.fill((0,0,0)) #predictably, filled with black.

	pygame.font.init() #to draw on the screen
	font = pygame.font.SysFont('comicsans', 60)
	label = font.render('Tetris', 1, (255,255,255)) #'1' for antialiasing; read up on that.

	surface.blit(label, (top_left_x + play_width/2 - label.get_width()/2, 30)) #.blit plays a role in loading an image.
													# that positioning gives the middle of the screen.
													# decided to hard code in the y axis at 50.
	draw_grid(surface,grid)
	pygame.display.update()  # updates the screen


def main(): #looks like elements of game play coming together
	locked_positions = {} # the dictonary from up above
	grid = create_grid(locked_positions)

	change_piece = False
	run = True
	current_piece = get_shape()
	next_piece = get_shape()
	clock = pygame.time.Clock()
	fall_tiem = 0

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					current_piece.x -= 1
				if event.key == pygame.K_RIGHT:
					current_piece.x += 1
				if event.key == pygame.K_DOWN:
					current_piece.y += 1
				if event.key == pygame.K_UP:

def main_menu():
	pass

main_menu()  # start game
