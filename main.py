import pygame as game
from pygame.locals import *
import sys

FPS = 20
black 		= (000, 000, 000)
white 		= (255, 255, 255)
red   		= (255, 000, 000)
blue  		= (000, 000, 255)
blueviolet 	= (138,  43, 226)
crimson 	= (220,  20,  60)
tomato		= (255,  99,  71)
pink = (255,   192,   203 )

TITLE = "Tic Tac Toe"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
BOARD_SIZE = 350

BOARD_CORNER_X = (WINDOW_WIDTH - BOARD_SIZE) / 2
BOARD_CORNER_Y = (WINDOW_HEIGHT - BOARD_SIZE) / 2
BOARD_CORNER_XY = (BOARD_CORNER_X, BOARD_CORNER_Y)
LINE_WIDTH = 5
WIN_LINE_WIDTH = 10
BLOCK_MARGIN = 25
SYMBOL_SIZE = BOARD_SIZE / 3 - 2 * BLOCK_MARGIN

WINDOW_BG_COLOR = pink #blueviolet
BLOCK_BG_COLOR = tomato #white
COLOR_OF_X = red
COLOR_OF_O = blue

TIE_TEXT = "It's a tie."
WIN_TEXT = lambda winner: f"{winner} has won!"
TEXT_FONT_TUPLE = ('Cambria', 40)
TEXT_Y = 50

RESTART_TEXT = "RESTART"
RESTART_TEXT_FONT_TUPLE = ('ariel', 32)
RESTART_TEXT_Y = 500 - 50
RESTART_TEXT_COLOR = white
RESTART_TEXT_BUTTON_COLOR = crimson
RESTART_TEXT_BUTTON_HOVER_COLOR = tomato
BUTTON_MARGIN = 8


class Symbols:
	@classmethod
	def symbol_X(cls):
		some_surface = game.Surface((SYMBOL_SIZE, SYMBOL_SIZE))
		some_surface.fill(BLOCK_BG_COLOR)
		game.draw.line(some_surface, COLOR_OF_X, (0, 0), (SYMBOL_SIZE, SYMBOL_SIZE), 8)
		game.draw.line(some_surface, COLOR_OF_X, (SYMBOL_SIZE, 0), (0, SYMBOL_SIZE), 8)
		return some_surface

	@classmethod
	def symbol_O(cls):
		some_surface = game.Surface((SYMBOL_SIZE, SYMBOL_SIZE))
		some_surface.fill(BLOCK_BG_COLOR)
		half_symbol_size = int(SYMBOL_SIZE / 2)
		game.draw.circle(some_surface, COLOR_OF_O, (half_symbol_size, half_symbol_size), half_symbol_size, 8)
		return some_surface

	@classmethod
	def draw_symbol(cls, screen, sym, pos):
		if sym == 'X':
			some_surface = cls.symbol_X()
		elif sym == 'O':
			some_surface = cls.symbol_O()
		else: return
		screen.blit(some_surface, pos)

class MyGame:
	symbols = ['X', 'O']

	def __init__(self):
		# Each cell of grid contains "", "X", or "O"
		# It looks exactly like the tic tac toe board
		self.grid = [["" for j in range(3)] for i in range(3)]

		# Whose turn is it now? False -> "X", True -> "O"
		self.turn = False 

		# Boolean signifying whether move has just been made
		self.just_updated = False # Not being used in multiple methods right now

		# Game status. 0 -> Playing 1 -> Over with Win 2 -> Over with Tie
		self.game_status = 0

		# Information about location of win
		self.win_line = None

		# No. of symbols on the board
		self.nf_symbols_on_board = 0

		game.init()
		self.screen = game.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		game.display.set_caption(TITLE)
		self.screen.fill(WINDOW_BG_COLOR)
		self.clock = game.time.Clock()

		self.TEXT_FONT = game.font.SysFont(*TEXT_FONT_TUPLE)
		self.RESTART_TEXT_FONT = game.font.SysFont(*RESTART_TEXT_FONT_TUPLE)
		self.create_restart_button()

	def play(self):
		while True:
			self.draw_board()
			self.draw_blocks()
			self.display_text()
			self.draw_restart_button()
			self.handle_events()
			if self.game_status == 1:
				self.draw_win_line()

			self.clock.tick(FPS)
			game.display.update()

	def register_move(self, mouse_position):
		self.just_updated = self.update_blocks(mouse_position)
	
		if self.just_updated:
			if self.has_been_won():
				self.game_status = 1
			elif self.nf_symbols_on_board == 3 * 3:
				self.game_status = 2
			else:
				self.turn = not self.turn
			#print(self.grid)	

	def handle_events(self):
		self.just_updated = False	
		for event in game.event.get():
			if event.type == QUIT:
				game.quit()
				sys.exit()

			elif event.type == game.MOUSEMOTION:
				# When the user clicks on a block
				if self.restart_button['button_rect'].collidepoint(event.pos):
					self.restart_button['color'] = RESTART_TEXT_BUTTON_HOVER_COLOR
				else:
					self.restart_button['color'] = RESTART_TEXT_BUTTON_COLOR


			elif event.type == game.MOUSEBUTTONDOWN:
				# When the user clicks on a block
				if self.restart_button['button_rect'].collidepoint(event.pos):
					self.restart_button['callback']()
				
				elif self.game_status == 0:
					self.register_move(event.pos)
				
				
	def draw_board(self):
		# Draws the # board itself without filling in anything
		board = game.Rect(BOARD_CORNER_XY, (BOARD_SIZE, BOARD_SIZE))
		game.draw.rect(self.screen, BLOCK_BG_COLOR, board)

		vertical_line_one_x = BOARD_CORNER_X + BOARD_SIZE / 3
		vertical_line_two_x = BOARD_CORNER_X + 2 * BOARD_SIZE / 3
		horizontal_line_one_y = BOARD_CORNER_Y + BOARD_SIZE / 3
		horizontal_line_two_y = BOARD_CORNER_Y + 2 * BOARD_SIZE / 3

		vertical_line = lambda x: (
						(x, BOARD_CORNER_Y), 
						(x, BOARD_CORNER_Y + BOARD_SIZE)
					)
		horizontal_line = lambda y: (
						(BOARD_CORNER_X, y), 
						(BOARD_CORNER_X + BOARD_SIZE, y)
					)

		my_four_lines = [vertical_line(vertical_line_one_x),
						 vertical_line(vertical_line_two_x),
						 horizontal_line(horizontal_line_one_y), 
						 horizontal_line(horizontal_line_two_y)]

		for line_start, line_stop in my_four_lines:
			game.draw.line(self.screen, WINDOW_BG_COLOR, line_start, line_stop, LINE_WIDTH)

	def display_text(self):
		if self.game_status == 1:
			text_to_print = WIN_TEXT(self.symbols[self.turn])
		elif self.game_status == 2:
			text_to_print = TIE_TEXT
		else: return

		text = self.TEXT_FONT.render(text_to_print, True, black)
		text_rect = text.get_rect(center = (WINDOW_WIDTH // 2, TEXT_Y))
		self.screen.blit(text, text_rect)

	def create_restart_button(self):
		button_color = RESTART_TEXT_BUTTON_COLOR
		center = (WINDOW_WIDTH // 2, RESTART_TEXT_Y)
		margin = BUTTON_MARGIN

		text = self.RESTART_TEXT_FONT.render(RESTART_TEXT, True, RESTART_TEXT_COLOR)
		text_rect = text.get_rect(center = center)

		my_button_rect = game.Rect(
			text_rect.x - margin, 
			text_rect.y - margin,
			text_rect.width + 2 * margin,
			text_rect.height + 2 * margin,
			)
		self.restart_button = {
			'text': text,
			'text_rect': text_rect,
			'button_rect': my_button_rect,
			'color': RESTART_TEXT_BUTTON_COLOR,
			'callback': self.__init__
		}

	def draw_restart_button(self):
		game.draw.rect(
			self.screen, 
			self.restart_button['color'], 
			self.restart_button['button_rect']
			)
		self.screen.blit(
			self.restart_button['text'],
			self.restart_button['text_rect'],
			)

	def update_blocks(self, mouse_position):
		# Updates self.grid based on where the user clicked
		box_size = BOARD_SIZE / 3
		valid_update = False
	
		for i in range(3): 
			for j in range(3):

				left = BOARD_CORNER_X + j * box_size
				top = BOARD_CORNER_Y + i * box_size
				box_rect = game.Rect(left, top, box_size, box_size)

				# If user clicked on this block
				if box_rect.collidepoint(mouse_position):

					if self.grid[i][j] == "": 
					# There is no symbol in this block
				
						self.grid[i][j] = self.symbols[self.turn]
						self.nf_symbols_on_board += 1
						valid_update = True
						break

					else: # There is already a symbol in this block
						valid_update = False
						break

		return valid_update


	def has_been_won(self):
		row_win = lambda i: (
			self.grid[i][0] == self.grid[i][1] == self.grid[i][2] != ""
			)
		col_win = lambda i: (
			self.grid[0][i] == self.grid[1][i] == self.grid[2][i] != ""
			)
		left_diag_win = lambda: (
			self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != ""
			)
		right_diag_win = lambda: (
			self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != ""
			)

		for i in range(3):
		
			if row_win(i):
				self.win_line = ("row", i)
				return True
		
			elif col_win(i):
				self.win_line = ("col", i)
				return True
		
		if left_diag_win():
			self.win_line = ("ldiag",)
			return True
		
		elif right_diag_win():
			self.win_line = ("rdiag",)
			return True
		
		return False

	def draw_win_line(self):
		assert self.win_line is not None
		#print(self.win_line)

		box_size = BOARD_SIZE / 3

		if self.win_line[0] == "col":
			i = self.win_line[1]
			
			start_pos = (
				BOARD_CORNER_X + (i + 0.5) * box_size, 
				BOARD_CORNER_Y
				)
			end_pos = (
				start_pos[0], 
				start_pos[1] + BOARD_SIZE
				)

		elif self.win_line[0] == "row":
			i = self.win_line[1]
			
			start_pos = (
				BOARD_CORNER_X, 
				BOARD_CORNER_Y + (i + 0.5) * box_size, 
				)
			end_pos = (
				start_pos[0] + BOARD_SIZE, 
				start_pos[1], 
				)

		elif self.win_line[0] == "ldiag":
			
			start_pos = (
				BOARD_CORNER_X, 
				BOARD_CORNER_Y,
				)
			end_pos = (
				BOARD_CORNER_X + BOARD_SIZE, 
				BOARD_CORNER_Y + BOARD_SIZE, 
				)

		elif self.win_line[0] == "rdiag":
			
			start_pos = (
				BOARD_CORNER_X + BOARD_SIZE, 
				BOARD_CORNER_Y,
				)
			end_pos = (
				BOARD_CORNER_X, 
				BOARD_CORNER_Y + BOARD_SIZE, 
				)

		game.draw.line(self.screen, black, start_pos, end_pos, WIN_LINE_WIDTH)


	def draw_blocks(self):

		box_size = BOARD_SIZE / 3
	
		for i in range(3):
			for j in range(3):
				left = BOARD_CORNER_X + j * box_size + BLOCK_MARGIN
				top = BOARD_CORNER_Y + i * box_size + BLOCK_MARGIN
				pos = (left, top)
				Symbols.draw_symbol(self.screen, self.grid[i][j], pos)

if __name__ == "__main__":
	MyGame().play()