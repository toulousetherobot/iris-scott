"""
Created on April 15, 2017
@author: aramael
"""
import pygame
from pygame.locals import *

import ui.fonts
import ui.colours
from ui.utilities import FilledRoundedRectangle

CURVES_FOLDER = "curves"

BUTTON_TITLE_FONT = ui.fonts.SF_UI_TEXT_LIGHT_FOOTNOTE
BUTTON_TEXT_COLOUR = ui.colours.PHOSPHORIC_TEXT_COLOR
BUTTON_BG_COLOUR = ui.colours.PHOSPHORIC_COLORS
BUTTON_XSIZE = ui.WINDOWWIDTH - ui.UI_MARGIN*2
BUTTON_YSIZE = 36
BUTTON_YGAP = 4
BUTTON_TEXT_MARGIN = 2 * BUTTON_YGAP

BUTTON_FILE = 1

def rounded_button(surface, button, x, y, 
	width=BUTTON_XSIZE,  height=BUTTON_YSIZE, 
	title_font=BUTTON_TITLE_FONT, text_color=BUTTON_TEXT_COLOUR,
	backround_color=BUTTON_BG_COLOUR):

	button_rect = FilledRoundedRectangle(surface, (x, y, width, height), backround_color, 0.4)

	# Header
	button_text_surf = title_font.render(button, True, text_color)
	button_text_rect = button_text_surf.get_rect()
	button_text_rect.midleft = (x + BUTTON_TEXT_MARGIN, y + height/2)
	surface.blit(button_text_surf, button_text_rect)

	return {"target": button_rect, "value": BUTTON_FILE, "action": button}