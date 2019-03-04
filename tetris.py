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
		for j in range(len(grid[i])): #whichever of those 1 to 20 you find yourself in.
			if (j,i) in locked_pos: #note that j is x value and i is y value
				c = locked_pos[(j,i)] #determining the x and y coordinates of what is locked and passing in those keys from the dictionary.
				grid[i][j] = c #finally, translating that locked cell to indexes related to the for loops. [i] was the outer for loop.
	return grid # "returned to whereer we're calling it from". Hopefully that is answered.

def convert_shape_format(shape):  # the goal here is to convert the dots and zeros into a form meaningful to Python.
	positions = []  #by putting positions in a list, there are numerous things we can do with them.
	format = shape.shape[shape.rotation % len(shape.shape)] #The modulus tells us which of the "sub" lists (by index) we'll use.
															#It seems shape.shape is each of the "letter" items.
															#then, shape.rotation is determined by the index of the  
															#sublist (starting at 0 but up to 3) that is used to 
															#reposition the piece as it descends. The len of shape.shape could be
															#anything between 1 and 4 possibiliites long. Unsure of this.
															#Shoddy, confusing naming convention at work here.

	for i, line in enumerate(format):   #format is what contains the 0s and 1s that constitute the shapes (it's also a keyword).
		row = list(line)                #passes in i and line in to enumerate: "for every i in line'; "index:item" or "counter:element".
		for j, column in enumerate(row):	 # lists gives back the info in a readable way.							
			if column == '0':			# Makes sense: any 0 indicates the beginning of whatever shape.
				positions.append((shape.x + j, shape.y + i)) #what *precisely* are 'shape.x' and 'shape.y'? Unsure of this.
									# General comments:
										# Enumerate produces tuples; basically, a "supplemented" for loop.
										# First you divide it up into rows on the y axis, then into columns by taking in rows. 
										# "'j' will be 0 and 'column' will be a period." Won't 'j' just be a column with a 0?
		
		#he's mumbling, but it sounds like this is to build "an offset"
		for i, pos in enumerate(positions):
			positions[i] = (pos[0] - 2, pos[1] - 4) # Will move everything left and up. Seems it's *not* using indexes.
													
		# what I think he's going for here is the coordinate 'x' in conjunction with the column index. Maybe.
												
def valid_space(shape, grid):
	accepted_pos = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)] # a two dimensional list
	accepted_pos = [j for sub in accepted_pos for j in sub] # flattening and overriding that into a one dimensional list (easier to loop through)
															# if statement only allows a position if a spot is gray (unoccupied)
	formatted = convert_shape_format(shape)

	for pos in formatted:
		if pos not in accepted_pos:
			if pos[1] > -1: # shapes will spawn north of the y axis. Here you are making sure it's greater than 0
				return False	#iow, "are we on the grid or not?"
	return True


def check_lost(positions): #to see if any of the positions are above the screen (after which you presumbly lose the game)
	for pos in positions:
		x,y = pos # splitting up the tuple here.
		if y < 1: # if it's less then 0, then you are above the screen and have lost the game.
			return True
	return False

def get_shape():
	return Piece(5,0,random.choice(shapes))  #randomizes the shape we see falling down, using class Pieces, which takes in the three arguments.
									# the screen. Notice there is no argument for the outer function.

def draw_text_middle(text, size, color, surface):
	pass

def draw_grid(surface, grid):
	sx = top_left_x   # sx = starting x
	sy = top_left_y	  # sy = starting y	

	for i in range(len(range)):
		pygame.draw.line(surface, (128,128,128),(sx,sy+i*block_size), (sx+play_width, sy+ i*block_size)) #color, start postiion, end position (10 vertical, his count is off)
		for j in range(len(grid[i])):
				pygame.draw.line(surface, (128, 128, 128), (sx+j*block_size, sy), (sx+j*block_size, sy+play_height))  #color, start postiion, end position (20 horizontal, his count is off) 


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
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size,top_left_y + i*block_size, block_size, block_size), 0)
	# the point here is to loop through every color on the grid and apply it to the surface.
	# the 0 is to fill in the shape and not just draw a border for it. Why...???

	#for the red area delimiting the play area:
	pygame.draw.rect(surface, (255, 0, 0), (top_left_x,top_left_y, play_width, play_height), 5)

	draw_grid(surface,grid)
	pygame.display.update()  # updates the screen


def main(win): #looks like elements of game play coming together
	locked_positions = {} # the dictonary from up above
	grid = create_grid(locked_positions)

	change_piece = False
	run = True
	current_piece = get_shape()
	next_piece = get_shape()
	clock = pygame.time.Clock()
	fall_tiem = 0
	fall_speed = 0.27

	while run:
		grid = create_grid(locked_positions) #be mindful that we need to constantly update the grid
		fall_time += clock.get_rawtime()
		clock.time()

		if fall_time/1000 > fall_speed:
			fall_time = 0
			current_piece.y += 1
			if not(valid_space(current_piece, grid)) and current_piece.y > 0:
				current_piece.y -= 1 #basically undoes the move (since it is not allowed)
				change_piece = True

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					current_piece.x -= 1
					if not(valid_space(current_piece,grid)):
						current_piece += 1 #+1 to pretend the move never happened.
				if event.key == pygame.K_RIGHT:
					current_piece.x += 1
					if not(valid_space(current_piece, grid)):
						current_piece -= 1
				if event.key == pygame.K_DOWN:
					current_piece.y += 1
					if not(valid_space(current_piece, grid)):
						current_piece.y -= 1 #why does he specify .y here when correcting but not .x with the others?
				if event.key == pygame.K_UP:
					current_piece.rotation += 1
					if not(valid_space(current_piece, grid)): #rotation itself can cause mismatches.
						current_piece -= 1

		draw_window(win, grid)

def main_menu(win):
	main(win)


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game
