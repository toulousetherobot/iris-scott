"""
Created on April 27, 2017
@author: aramael
"""
import pygame
from pygame.locals import *

from . import settings
from . import fonts
from . import colours
from ui.utilities import FilledRoundedRectangle, Header, DrawTextBox

# Message Settings
MESSAGE_TITLE_FONT = fonts.SF_UI_TEXT_LIGHT_HEADER
MESSAGE_FOOTNOTE_FONT = fonts.SF_UI_TEXT_LIGHT_FOOTNOTE
MESSAGE_TEXT_COLOUR = colours.LIGHT_GRAY
MESSAGE_TITLE_MARGIN_TOP = 100
MESSAGE_FOOTNOTE_RECT = Rect((0, 0, 240, 60)) # , 68)) for 4 lines
MESSAGE_FOOTNOTE_RECT.midtop = (settings.WINDOWWIDTH/2, MESSAGE_TITLE_MARGIN_TOP+30)

BUTTON_ACKNOWLEDGE = 2

def message_display(surface, robot, title_font=MESSAGE_TITLE_FONT, footnote_font= MESSAGE_FOOTNOTE_FONT, text_color=MESSAGE_TEXT_COLOUR, footnote_text_rect=MESSAGE_FOOTNOTE_RECT):
	
	Header(surface, robot, "Home Axes", colours.WHITE)

	# Image
	icn_img = pygame.image.load("/home/pi/toulouseos/home_axes_63.png").convert_alpha()
	icn_img_rect = icn_img.get_rect()
	icn_img_rect.midtop = (settings.WINDOWWIDTH/2, settings.UI_MARGIN_TOP)
	surface.blit(icn_img, icn_img_rect)

	# Header
	button_text_surf = title_font.render("Home Axes", True, colours.INFO_BLUE)
	button_text_rect = button_text_surf.get_rect()
	button_text_rect.midtop = (settings.WINDOWWIDTH/2, MESSAGE_TITLE_MARGIN_TOP)
	surface.blit(button_text_surf, button_text_rect)

	# Footnote
	DrawTextBox(surface, "Before Toulouse can paint or sketch any jobs, the automatic homing sequence must be run.", text_color, footnote_text_rect, footnote_font, aa=True)

	# Buttons
	message_buttons = []

	# Acknowledge
	button_rect = Rect((0,0, settings.WINDOWWIDTH - 2 * settings.UI_MARGIN, 36))
	button_rect.topright = (settings.WINDOWWIDTH - settings.UI_MARGIN, footnote_text_rect.y+ footnote_text_rect.height)
	button_rect = FilledRoundedRectangle(surface, button_rect, colours.BUTTON_3_BG_COLOR, 0.4)
	message_buttons.append({"target": button_rect, "value": BUTTON_ACKNOWLEDGE})

	button_text_surf = fonts.SF_UI_DISPLAY_LIGHT.render("start", True, colours.BUTTON_3_TEXT_COLOR)
	button_text_rect = button_text_surf.get_rect()
	button_text_rect.center = button_rect.center
	surface.blit(button_text_surf, button_text_rect)

	return message_buttons