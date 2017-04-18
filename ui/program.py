"""
Created on April 9, 2017
@author: aramael
"""
import pygame
from pygame.locals import *

from . import settings
from . import fonts
from . import colours

from ui.utilities import FilledRoundedRectangle

BUTTON_TITLE_FONT = fonts.SF_UI_TEXT_LIGHT_HEADER
BUTTON_FOOTNOTE_FONT = fonts.SF_UI_TEXT_LIGHT_FOOTNOTE
BUTTON_TEXT_COLOUR = colours.PHOSPHORIC_TEXT_COLOR
BUTTON_BG_COLOUR = colours.PHOSPHORIC_COLORS
BUTTON_YSTART = settings.UI_MARGIN_TOP
BUTTON_XSTART = settings.UI_MARGIN_LEFT
BUTTON_XSIZE = settings.WINDOWWIDTH-settings.UI_MARGIN*2
BUTTON_YSIZE = 56
BUTTON_YGAP = 6
BUTTON_TEXT_MARGIN = 2 * BUTTON_YGAP

BUTTON_CARICATURE = 2
BUTTON_CURVES = 1

BUTTONS = [
	{
		"title": "Caricature",
		"footnote": "Take a Photo of a Guest & Draw",
		"value": BUTTON_CARICATURE},
	{
		"title": "Load Curves",
		"footnote": "Draw Provided Curves File",
		"value": BUTTON_CURVES},]

def rounded_button(surface, button, x, y, 
	width=BUTTON_XSIZE,  height=BUTTON_YSIZE, 
	title_font=BUTTON_TITLE_FONT, footnote_font=BUTTON_FOOTNOTE_FONT, 
	text_color=BUTTON_TEXT_COLOUR, backround_color=BUTTON_BG_COLOUR):

	button_rect = FilledRoundedRectangle(surface, (x, y, width, height), backround_color, 0.4)

	# Header
	button_text_surf = title_font.render(button["title"], True, text_color)
	button_text_rect = button_text_surf.get_rect()
	button_text_rect.bottomleft = (x + BUTTON_TEXT_MARGIN, y + 3*height/4 - 3)
	surface.blit(button_text_surf, button_text_rect)

	# Footer
	button_text_surf = footnote_font.render(button["footnote"], True, text_color)
	button_text_rect = button_text_surf.get_rect()
	button_text_rect.bottomleft = (x + BUTTON_TEXT_MARGIN, y + 3*height/4 + 10)
	surface.blit(button_text_surf, button_text_rect)

	return {"target": button_rect, "value": button["value"]}