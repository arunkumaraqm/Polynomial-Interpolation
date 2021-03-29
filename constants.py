FPS = 20 # frames per second

import pandas as pd

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

# window details
WINDOW_TITLE = "Computer Graphics Project"
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 800

# board details
BOARD_SIZE = 620
BOARD_CORNER_X = (WINDOW_WIDTH - BOARD_SIZE) / 2
BOARD_CORNER_Y = (WINDOW_HEIGHT - BOARD_SIZE) / 2
BOARD_CORNER_XY = (BOARD_CORNER_X, BOARD_CORNER_Y)
LINE_WIDTH = 5
WIN_LINE_WIDTH = 10
BLOCK_MARGIN = 25

# colour details
WINDOW_BG_COLOR = colors['blueviolet']
BOARD_BG_COLOR = colors['fafafa']

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

MODE_TEXT_Y = 50
