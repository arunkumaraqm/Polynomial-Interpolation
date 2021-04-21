import pygame as game
from pygame.locals import *
import sys
from collections import defaultdict
import numpy as np

from constants import *
from numerical_methods import NumericalMethods


class MyGame:
    def __init__(self):
        game.init()
        self.screen = game.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        game.display.set_caption(WINDOW_TITLE)
        self.screen.fill(WINDOW_BG_COLOR)
        self.clock = game.time.Clock()

        # initializing fonts
        self.TEXT_FONT = game.font.SysFont(*TEXT_FONT_TUPLE)  # not used for now
        self.RESTART_TEXT_FONT = game.font.SysFont(*RESTART_TEXT_FONT_TUPLE)
        self.MODE_TEXT_FONT = game.font.SysFont(*MODE_TEXT_FONT_TUPLE)

        self.mode_buttons = defaultdict(dict)
        self.create_restart_button()
        self.create_mode_buttons()

        board_rect = game.Rect(BOARD_CORNER_X, BOARD_CORNER_Y, BOARD_SIZE, BOARD_SIZE)
        inner_board_rect = game.Rect((BOARD_CORNER_X + 5), (BOARD_CORNER_Y + 5), INNER_BOARD_SIZE, INNER_BOARD_SIZE)
        self.board = {
            'rect': board_rect,
            'color': BOARD_BG_COLOR,
        }
        self.inner_board = {
            'rect': inner_board_rect,
            'color': WINDOW_BG_COLOR,
        }

        self.something_happened = True

        # important state variables
        self.points = []
        self.points_constituting_line = defaultdict(list)
        self.modes = set(['bezier'])

    def play(self):
        while True:
            # there is no need to calculate what pixels to fill
            # if most of the window remains unchanged
            if self.something_happened:
                self.screen.fill(WINDOW_BG_COLOR)
                self.draw_board()
                self.draw_lines()
                self.draw_points()
                self.draw_control_graph()
            # self.display_text()

            # drawing buttons
            self.draw_button(self.restart_button)
            for mode in ALL_MODES:
                self.draw_button(self.mode_buttons[mode])

            self.handle_events()
            self.clock.tick(FPS)
            game.display.update()

    def handle_events(self):
        self.something_happened = False

        for event in game.event.get():

            # when X is pressed
            if event.type == QUIT:
                game.quit()
                sys.exit()

            # when the mouse moves across the window
            elif event.type == game.MOUSEMOTION:
                if self.restart_button['button_rect'].collidepoint(event.pos):
                    self.restart_button['color'] = RESTART_TEXT_BUTTON_HOVER_COLOR
                else:
                    self.restart_button['color'] = RESTART_TEXT_BUTTON_COLOR

                # mode buttons' hover changes
                for mode in ALL_MODES:
                    if self.mode_buttons[mode]['button_rect'].collidepoint(event.pos):
                        self.mode_buttons[mode]['color'] = MODE_BUTTON_HOVER_BG_COLOR_MAP[mode]
                        self.mode_buttons[mode]['text'] = self.MODE_TEXT_FONT.render(mode.upper(), True, MODE_BUTTON_HOVER_TEXT_COLOR_MAP[mode])
                    else:
                        self.mode_buttons[mode]['color'] = MODE_BUTTON_BG_COLOR_MAP[mode]
                        self.mode_buttons[mode]['text'] = self.MODE_TEXT_FONT.render(mode.upper(), True, MODE_BUTTON_TEXT_COLOR_MAP[mode])


            # when the mouse is clicked but not released
            # the 'not released' part is irrelevant to us
            elif event.type == game.MOUSEBUTTONDOWN:
                self.something_happened = True

                # if restart button is clicked, call its callback function
                if self.restart_button['button_rect'].collidepoint(event.pos):
                    self.restart_button['callback']()

                # if board is clicked, add a point there
                elif self.inner_board['rect'].collidepoint(event.pos):
                    self.points.append(event.pos)

                # user is modifying active modes
                else:
                    for mode in ALL_MODES:
                        if self.mode_buttons[mode]['button_rect'].collidepoint(event.pos):
                            if mode in self.modes:
                                self.modes.discard(mode)
                            else:
                                self.modes.add(mode)

    def draw_board(self):
        # Draws the board itself without filling in anything
        board = game.Rect(BOARD_CORNER_XY, (BOARD_SIZE, BOARD_SIZE))
        game.draw.rect(self.screen, self.board['color'], board)

    def draw_points(self):
        color_of_point = COLOR_OF_POINT
        for pt in self.points:
            game.draw.circle(self.screen, color_of_point, pt, 6, width=5)

    def draw_line_dashed(
        self, 
        color, 
        start_pos, 
        end_pos, 
        width=1, 
        dash_length=10, 
        exclude_corners=True
    ):
        # taken from https://codereview.stackexchange.com/a/248823/233032

        # convert tuples to numpy arrays
        start_pos = np.array(start_pos)
        end_pos   = np.array(end_pos)

        # get euclidian distance between start_pos and end_pos
        length = np.linalg.norm(end_pos - start_pos)

        # get amount of pieces that line will be split up in (half of it are amount of dashes)
        dash_amount = int(length / dash_length)

        # x-y-value-pairs of where dashes start (and on next, will end)
        dash_knots = np.array([np.linspace(start_pos[i], end_pos[i], dash_amount) for i in range(2)]).transpose()

        exclude_corners = int(exclude_corners)
        for n in range(exclude_corners, dash_amount - exclude_corners, 2):
            game.draw.line(
                self.screen, 
                color, 
                tuple(dash_knots[n]), 
                tuple(dash_knots[n+1]), 
                width
            )


    def draw_control_graph(self):
        if len(self.modes) != 0 and self.modes.isdisjoint(MODES_NEEDING_CONTROL_GRAPH):
            return
        if len(self.points) > 2:
            for first, second in zip(self.points[:-1], self.points[1:]):
                self.draw_line_dashed(
                    COLOR_OF_CONTROL_GRAPH, 
                    first, 
                    second
                )

    def draw_lines(self):
        for mode in self.modes:
            try:
                # calling the correct numerical method to get points constituting the curve
                self.points_constituting_line[mode] = getattr(NumericalMethods, mode)(self.points)
                # filter out parts of curve lying outside board
                self.points_constituting_line[mode] = [
                    pt for pt in self.points_constituting_line[mode]
                    if self.inner_board['rect'].collidepoint(pt)
                ]
            except ValueError as er:
                print("Error: ", str(er))

        for mode in self.modes:
            color_of_line = MODE_LINE_COLOR_MAP[mode]
            for pt in self.points_constituting_line[mode]:
                game.draw.circle(self.screen, color_of_line, pt, 3, width=5)

    def connected(self):
        """ This function is not used anywhere. """
        for pt1 in self.points:
            for pt2 in self.points:
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
        text_rect = text.get_rect(center=center)

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
            'color': button_color,
            'callback': self.__init__
        }

    def create_mode_buttons(self):
        for i, mode in enumerate(ALL_MODES):
            button_color = MODE_BUTTON_BG_COLOR_MAP[mode]
            center = ((2 * i + 1) * (WINDOW_WIDTH // (2 * len(ALL_MODES))), MODE_TEXT_Y)
            margin = BUTTON_MARGIN

            text = self.MODE_TEXT_FONT.render(mode.upper(), True, MODE_BUTTON_TEXT_COLOR_MAP[mode])
            text_rect = text.get_rect(center=center)

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
