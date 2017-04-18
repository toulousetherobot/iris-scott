"""
Created on April 10, 2017
@author: aramael
"""
import pygame
# from pygame.locals import *
from pygame import gfxdraw # used in Main Menu
from math import ceil # used in Main Menu

from . import settings
from . import fonts
from . import colours

from .utilities import FilledRoundedRectangle, FilledCircle

BUTTON_TITLE_FONT = fonts.SF_UI_TEXT_LIGHT_HEADER
BUTTON_FOOTNOTE_FONT = fonts.SF_UI_TEXT_LIGHT_FOOTNOTE
BUTTON_TEXT_COLOUR = colours.WHITE
BUTTON_BG_COLOUR = colours.BUTTON_BG_COLOR
BUTTON_YSTART = settings.UI_MARGIN_TOP
BUTTON_XSTART = 30
BUTTON_XSIZE = settings.WINDOWWIDTH-settings.UI_MARGIN_LEFT-settings.UI_MARGIN_RIGHT
BUTTON_YSIZE = 56
BUTTON_YGAP = 6
BUTTON_TEXT_MARGIN = BUTTON_YSIZE + BUTTON_YGAP

BUTTON_LOCK = 3
BUTTON_RESTART = 2
BUTTON_SHUTDOWN = 1
BUTTON_CANCEL = 4

BUTTONS = [
	{
		"icon": "lock.png",
		"title": "Lock",
		"footnote": "Lock Toulouse Control Panel",
		"value": BUTTON_LOCK},
	{
		"icon": "restart.png",
		"title": "Restart",
		"footnote": "Power off & Restart Toulouse",
		"value": BUTTON_RESTART},
	{
		"icon": "shutdown.png",
		"title": "Shutdown",
		"footnote": "Power off Toulouse",
		"value": BUTTON_SHUTDOWN},]

def rounded_button(surface, button, x, y, 
	width=BUTTON_XSIZE,  height=BUTTON_YSIZE, 
	title_font=BUTTON_TITLE_FONT, footnote_font=BUTTON_FOOTNOTE_FONT, 
	text_color=BUTTON_TEXT_COLOUR, backround_color=BUTTON_BG_COLOUR):

	button_rect = FilledRoundedRectangle(surface, (x, y, width, height), backround_color, 1)
	
	# Circle
	circle = FilledCircle(surface, (ceil(BUTTON_YSIZE/2 + x), ceil(BUTTON_YSIZE/2 + y), ceil((BUTTON_YSIZE-BUTTON_YGAP))), ui.colours.WHITE)

	# Image
	img_splash = pygame.image.load(button["icon"]).convert_alpha()
	surface.blit(img_splash, (x, y))

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