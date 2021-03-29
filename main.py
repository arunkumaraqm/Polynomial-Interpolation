import pygame as game
from pygame.locals import *
import numpy as np
import sys
from collections import defaultdict

from constants import *

class NumericalMethods:
	@classmethod
	def lagrange(cls, pts):
		k = len(pts) - 1

		def lj_of_x(j, x):
			ret = 1

			for m in range(0, k + 1):
				xm = pts[m][0]
				xj = pts[j][0]

				if m != j:
					ret *= (x - xm)/(xj - xm)

			return ret

		def L(x):
			summ = 0
			for j in range(0, k + 1):
				yj = pts[j][1]
				summ += yj * lj_of_x(j, x)
			return summ

		if len(pts):
			xmin = min(pts, key=lambda pt: pt[0])[0]
			xmax = max(pts, key=lambda pt: pt[0])[0]

			return [ (xi, L(xi)) for xi in np.arange(xmin, xmax + 1, 0.1)]
		else:
			return []

	bezier = lagrange
	hermite = lagrange


MODE_POINT_COLOR_MAP = {
	'connected': 		colors['sap_green'],
	'lagrange': 		colors['red'],
	'bezier':			colors['medium_red_violet'],
	'hermite':			colors['honolulu_blue'],
}
MODE_LINE_COLOR_MAP = {
	'connected':		colors['raspberry'],
	'lagrange': 		colors['yellow'],
	'bezier':			colors['green_yellow'],
	'hermite':			colors['mauve'],
}

all_modes = ['lagrange', 'bezier', 'hermite']

class MyGame:
	def __init__(self):
		game.init()
		self.screen = game.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		game.display.set_caption(WINDOW_TITLE)
		self.screen.fill(WINDOW_BG_COLOR)
		self.clock = game.time.Clock()

		self.TEXT_FONT = game.font.SysFont(*TEXT_FONT_TUPLE)
		self.RESTART_TEXT_FONT = game.font.SysFont(*RESTART_TEXT_FONT_TUPLE)

		self.mode_buttons = defaultdict(dict)
		self.create_restart_button()
		self.create_mode_buttons()

		board_rect = game.Rect(BOARD_CORNER_X, BOARD_CORNER_Y, BOARD_SIZE, BOARD_SIZE)

		self.board = {
			'rect': board_rect,
			'color': BOARD_BG_COLOR,
		}

		self.something_happened = True	
		self.points = defaultdict(list)
		self.points_constituting_line = defaultdict(list)
		self.mode = 'lagrange'

	def play(self):
		while True:
			# there is no need to calculate what pixels to fill 
			# if most of the window remains unchanged
			if self.something_happened: 
				self.screen.fill(WINDOW_BG_COLOR)
				self.draw_board()
				self.draw_lines()
				self.draw_points()
				# self.display_text()
			self.draw_button(self.restart_button)
			for mode in all_modes: self.draw_button(self.mode_buttons[mode])

			self.handle_events()
			self.clock.tick(FPS)
			game.display.update()

	def handle_events(self):
		self.something_happened = False	

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
				self.something_happened = True

				# if restart button is clicked, call its callback function
				if self.restart_button['button_rect'].collidepoint(event.pos):
					self.restart_button['callback']()
		
				# if board is clicked, add a point there
				elif self.board['rect'].collidepoint(event.pos):
					self.points[self.mode].append(event.pos)

				else:
					for mode in all_modes:
						if self.mode_buttons[mode]['button_rect'].collidepoint(event.pos):
							self.mode = mode
				
				
	def draw_board(self):
		# Draws the board itself without filling in anything
		board = game.Rect(BOARD_CORNER_XY, (BOARD_SIZE, BOARD_SIZE))
		game.draw.rect(self.screen, self.board['color'], board)

	def draw_points(self):
		for mode in all_modes:
			color_of_point = MODE_POINT_COLOR_MAP[mode]
			for pt in self.points[mode]:
				game.draw.circle(self.screen, color_of_point, pt, 6, width=5)

	def draw_lines(self):
		self.points_constituting_line[self.mode] = getattr(NumericalMethods, self.mode)(self.points[self.mode])

		for mode in all_modes:
			color_of_line = MODE_LINE_COLOR_MAP[mode]
			for pt in self.points_constituting_line[mode]:
				game.draw.circle(self.screen, color_of_line, pt, 3, width=5)

	def connected(self):
		""" This function is not used anywhere. """
		for pt1 in self.points['connected']:
			for pt2 in self.points['connected']:
				game.draw.aaline(self.screen, MODE_LINE_COLOR_MAP[self.mode], pt1, pt2)



	# def display_text(self):
	# 	if self.game_status == 1:
	# 		text_to_print = WIN_TEXT(self.symbols[self.turn])
	# 	elif self.game_status == 2:
	# 		text_to_print = TIE_TEXT
	# 	else: return
	# 
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

	def create_mode_buttons(self):
		for i, mode in enumerate(all_modes):
			button_color = MODE_LINE_COLOR_MAP[mode]
			center = ((2*i+1) * (WINDOW_WIDTH // (2 * len(all_modes))), MODE_TEXT_Y)
			margin = BUTTON_MARGIN

			text = self.RESTART_TEXT_FONT.render(mode.upper(), True, MODE_POINT_COLOR_MAP[mode])
			text_rect = text.get_rect(center = center)

			my_button_rect = game.Rect(
				text_rect.x - margin, 
				text_rect.y - margin,
				text_rect.width + 2 * margin,
				text_rect.height + 2 * margin,
			)

			self.mode_buttons[mode] = {
				'text': text,
				'text_rect': text_rect,
				'button_rect': my_button_rect,
				'color': button_color
			}

	def draw_button(self, given_button):
		game.draw.rect(
			self.screen, 
			given_button['color'], 
			given_button['button_rect']
		)
		self.screen.blit(
			given_button['text'],
			given_button['text_rect'],
		)

if __name__ == "__main__":
	MyGame().play()