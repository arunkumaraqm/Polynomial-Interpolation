FPS = 20 # frames per second

import pandas as pd
import pygame as game

cdf = pd.read_csv('colors.csv')

# convert to dictionary with name as key and list of r, g, b values as value
del cdf['common_name']
del cdf['hex']
colors = cdf.set_index('name').T.to_dict('list')


colors.update({
	'black': 		(000, 000, 000),
	'white': 		(255, 255, 255),
	'fafafa': 		(250, 250, 250),
	'red':   		(255, 000, 000),
	'blue':  		(000, 000, 255),
	'yellow': 		(255, 255, 000),
	'blueviolet': 	(138,  43, 226),
	'crimson':	 	(220,  20,  60),
	'tomato':		(255,  99,  71),
	'pink': 		(255, 192, 203),
})

# mode names and point and line colours
ALL_MODES = ['lagrange', 'bezier', 'cardinal']

# window details
WINDOW_TITLE = "Computer Graphics Project"
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 650

# board details
BOARD_SIZE = 500
INNER_BOARD_SIZE = 480
BOARD_CORNER_X = (WINDOW_WIDTH - BOARD_SIZE) / 2
BOARD_CORNER_Y = (WINDOW_HEIGHT - BOARD_SIZE) / 2
BOARD_CORNER_XY = (BOARD_CORNER_X, BOARD_CORNER_Y)

# colour details
WINDOW_BG_COLOR = colors['blueviolet']
BOARD_BG_COLOR = colors['fafafa']
COLOR_OF_POINT = colors['medium_red_violet']
MODE_LINE_COLOR_MAP = {
	'connected':		colors['raspberry'],
	'lagrange': 		colors['yellow'],
	'bezier':			colors['green_yellow'],
	'cardinal':			colors['mauve'],
} # given mode, what should be the colour of the curve?

CONTROL_GRAPH_REQUIRED = {
	'connected':	False,
	'lagrange':		False,
	'bezier':		True,
	'cardinal':		True,
}
MODES_NEEDING_CONTROL_GRAPH = set(key for key, value in CONTROL_GRAPH_REQUIRED.items() if value is True)

# text details
TEXT_FONT_TUPLE = ('Cambria', 40)

# restart button details
RESTART_TEXT = "RESTART"
RESTART_TEXT_FONT_TUPLE = ('ariel', 32)
RESTART_TEXT_Y = WINDOW_HEIGHT - 50
RESTART_TEXT_COLOR = colors['white']
RESTART_TEXT_BUTTON_COLOR = colors['crimson']
RESTART_TEXT_BUTTON_HOVER_COLOR = colors['tomato']
BUTTON_MARGIN = 8

# mode button details
MODE_TEXT_FONT_TUPLE = ('ariel bold', 32)
MODE_OFF_TEXT_FONT_TUPLE = ('ariel', 32)
MODE_TEXT_Y = 50
MODE_BUTTON_TEXT_COLOR_MAP = {
	'connected': 		colors['sap_green'],
	'lagrange': 		colors['red'],
	'bezier':			colors['medium_red_violet'],
	'cardinal':			colors['honolulu_blue'],
}
# text color changes on hover
MODE_BUTTON_HOVER_TEXT_COLOR_MAP = {
	'connected':		colors['raspberry'],
	'lagrange': 		colors['yellow'],
	'bezier':			colors['green_yellow'],
	'cardinal':			colors['mauve'],
}

# button bg color changes on hover
MODE_BUTTON_HOVER_BG_COLOR_MAP = {
	'connected': 		colors['sap_green'],
	'lagrange': 		colors['red'],
	'bezier':			colors['medium_red_violet'],
	'cardinal':			colors['honolulu_blue'],
}

MODE_BUTTON_BG_COLOR_MAP = MODE_LINE_COLOR_MAP # given mode, what should be the background colour of this mode's button?

# MODE_INDICATOR_TEXT_FONT_TUPLE = ('ariel', 16)
# MODE_INDICATOR_COLOR = colors['white']

# to add
# point radius and point width for points and points constituting lines

COLOR_OF_CONTROL_GRAPH = colors['fluorescent_pink']

