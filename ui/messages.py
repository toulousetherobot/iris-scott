"""
Created on April 16, 2017
@author: aramael
"""
import pygame
from pygame.locals import *

import ui.fonts
import ui.colours
from ui.utilities import FilledRoundedRectangle

BUTTON_TITLE_FONT = ui.fonts.SF_UI_TEXT_LIGHT_HEADER
BUTTON_FOOTNOTE_FONT = ui.fonts.SF_UI_TEXT_LIGHT_FOOTNOTE
BUTTON_TEXT_COLOUR = ui.colours.WHITE
BUTTON_BG_COLOUR = ui.colours.BUTTON_BG_COLOR
BUTTON_XSTART = 30
BUTTON_XSIZE = ui.WINDOWWIDTH-ui.UI_MARGIN*2
BUTTON_YSIZE = 56
BUTTON_YGAP = 6
BUTTON_TEXT_MARGIN = 4 * BUTTON_YGAP
BUTTON_READ_MARGIN = 1 * BUTTON_YGAP


BUTTONS = [
	{
		"type": "warning",
		"read": False,
		"title": "Limit Switch Hit",
		"footnote": "Shoulder Pan Left Limit Switch Hit.",
		"value": 1},
	{
		"type": "error",
		"read": True,
		"title": "Emergency Stop",
		"footnote": "Shoulder Pan Left Limit Switch Hit.",
		"value": 1},
	{
		"type": "info",
		"read": False,
		"title": "Photo Taken",
		"footnote": "Shoulder Pan Left Limit Switch Hit.",
		"value": 1},
	{
		"type": "success",
		"read": False,
		"title": "Loaded Program",
		"footnote": "Shoulder Pan Left Limit Switch Hit.",
		"value": 1},]

def rounded_button(surface, button, x, y, 
	width=BUTTON_XSIZE,  height=BUTTON_YSIZE, 
	title_font=BUTTON_TITLE_FONT, footnote_font=BUTTON_FOOTNOTE_FONT, 
	text_color=BUTTON_TEXT_COLOUR, backround_color=BUTTON_BG_COLOUR):

	button_rect = FilledRoundedRectangle(surface, (x, y, width, height), backround_color, 0.4)

	if button["type"] == "info":
		notification_color = ui.colours.INFO_BLUE
		icon_img = "info_icn_42.png"
	elif button["type"] == "success":
		notification_color = ui.colours.SUCCESS_GREEN
		icon_img = "success_icn_42.png"
	elif button["type"] == "warning":
		notification_color = ui.colours.WARNING_ORANGE
		icon_img = "warning_icn_42.png"
	elif button["type"] == "error":
		notification_color = ui.colours.ERROR_RED
		icon_img = "error_icn_42.png"
	else:
		notification_color = ui.colours.WHITE

	if (not button["read"]):
		FilledRoundedRectangle(surface, (x+BUTTON_READ_MARGIN, y+BUTTON_YGAP, BUTTON_YGAP, height-BUTTON_YGAP*2), notification_color, 1)

	# Image
	icn_img = pygame.image.load(icon_img).convert_alpha()
	icn_img_rect = icn_img.get_rect()
	icn_img_rect.midright = (x+width-BUTTON_YGAP, y + height/2)
	surface.blit(icn_img, icn_img_rect)

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