import pygame as game
from pygame.locals import *
import sys

import numpy as np

FPS = 20
black 		= (000, 000, 000)
white 		= (255, 255, 255)
fafafa 		= (250, 250, 250)
red   		= (255, 000, 000)
blue  		= (000, 000, 255)
yellow 		= (255, 255, 000)
blueviolet 	= (138,  43, 226)
crimson 	= (220,  20,  60)
tomato		= (255,  99,  71)
pink 		= (255, 192, 203)

TITLE = "Computer Graphics Project"
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 800
BOARD_SIZE = 620

BOARD_CORNER_X = (WINDOW_WIDTH - BOARD_SIZE) / 2
BOARD_CORNER_Y = (WINDOW_HEIGHT - BOARD_SIZE) / 2
BOARD_CORNER_XY = (BOARD_CORNER_X, BOARD_CORNER_Y)
LINE_WIDTH = 5
WIN_LINE_WIDTH = 10
BLOCK_MARGIN = 25
SYMBOL_SIZE = BOARD_SIZE / 3 - 2 * BLOCK_MARGIN

WINDOW_BG_COLOR = blueviolet
BOARD_BG_COLOR = fafafa
COLOR_OF_POINT = red
COLOR_OF_LINE = blue

TEXT_FONT_TUPLE = ('Cambria', 40)

RESTART_TEXT = "RESTART"
RESTART_TEXT_FONT_TUPLE = ('ariel', 32)
RESTART_TEXT_Y = WINDOW_HEIGHT - 50
RESTART_TEXT_COLOR = white
RESTART_TEXT_BUTTON_COLOR = crimson
RESTART_TEXT_BUTTON_HOVER_COLOR = tomato
BUTTON_MARGIN = 8

class MyGame:
	symbols = ['X', 'O']

	def __init__(self):
		game.init()
		self.screen = game.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		game.display.set_caption(TITLE)
		self.screen.fill(WINDOW_BG_COLOR)
		self.clock = game.time.Clock()

		board_rect = game.Rect(BOARD_CORNER_X, BOARD_CORNER_Y, BOARD_SIZE, BOARD_SIZE)

		self.board = {
			'rect': board_rect,
			'color': BOARD_BG_COLOR,
		}

		self.points = []

		self.TEXT_FONT = game.font.SysFont(*TEXT_FONT_TUPLE)
		self.RESTART_TEXT_FONT = game.font.SysFont(*RESTART_TEXT_FONT_TUPLE)
		self.create_restart_button()

	def play(self):
		while True:
			self.screen.fill(WINDOW_BG_COLOR)
			self.draw_board()
			self.draw_lines()
			self.draw_points()
			# self.display_text()
			self.draw_restart_button()
			self.handle_events()

			self.clock.tick(FPS)
			game.display.update()

	def handle_events(self):
		self.just_updated = False	
		for event in game.event.get():
			if event.type == QUIT:
				game.quit()
				sys.exit()

			elif event.type == game.MOUSEMOTION:
				if self.restart_button['button_rect'].collidepoint(event.pos):
					self.restart_button['color'] = RESTART_TEXT_BUTTON_HOVER_COLOR
				else:
					self.restart_button['color'] = RESTART_TEXT_BUTTON_COLOR


			elif event.type == game.MOUSEBUTTONDOWN:
				if self.restart_button['button_rect'].collidepoint(event.pos):
					self.restart_button['callback']()
		
				elif self.board['rect'].collidepoint(event.pos):
					self.points.append(event.pos)
				
				
	def draw_board(self):
		# Draws the # board itself without filling in anything
		board = game.Rect(BOARD_CORNER_XY, (BOARD_SIZE, BOARD_SIZE))
		game.draw.rect(self.screen, BOARD_BG_COLOR, board)

	def draw_points(self):
		for pt in self.points:
			game.draw.circle(self.screen, COLOR_OF_POINT, pt, 6, width=5)

	def draw_lines(self):
		# for pt1 in self.points:
		# 	for pt2 in self.points:
		# 		game.draw.aaline(self.screen, COLOR_OF_LINE, pt1, pt2)

		k = len(self.points) - 1

		def lj_of_x(j, x):
			ret = 1

			for m in range(0, k + 1):
				xm = self.points[m][0]
				xj = self.points[j][0]

				if m != j:
					ret *= (x - xm)/(xj - xm)

			return ret

		def L(x):
			summ = 0
			for j in range(0, k + 1):
				yj = self.points[j][1]
				summ += yj * lj_of_x(j, x)
			return summ

		if len(self.points):
			xmin = min(self.points, key=lambda pt: pt[0])[0]
			xmax = max(self.points, key=lambda pt: pt[0])[0]

			for xi in np.arange(xmin, xmax + 1, 0.1):
				game.draw.circle(self.screen, yellow, (xi, L(xi)), 3, width=5)
				# print(xi, lag_poly(xi))



	# def display_text(self):
	# 	if self.game_status == 1:
	# 		text_to_print = WIN_TEXT(self.symbols[self.turn])
	# 	elif self.game_status == 2:
	# 		text_to_print = TIE_TEXT
	# 	else: return

	# 	text = self.TEXT_FONT.render(text_to_print, True, black)
	# 	text_rect = text.get_rect(center = (WINDOW_WIDTH // 2, TEXT_Y))
	# 	self.screen.blit(text, text_rect)

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
					self.grid[i][j] = self.symbols[self.turn]
					self.nf_symbols_on_board += 1
					valid_update = True
					break

		return valid_update



if __name__ == "__main__":
	MyGame().play()