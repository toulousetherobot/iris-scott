"""
Created on April 16, 2017
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

# Button Settings
BUTTON_TITLE_FONT = fonts.SF_UI_TEXT_LIGHT_HEADER
BUTTON_FOOTNOTE_FONT = fonts.SF_UI_TEXT_LIGHT_FOOTNOTE
BUTTON_TEXT_COLOUR = colours.WHITE
BUTTON_BG_COLOUR = colours.BUTTON_BG_COLOR
BUTTON_XSTART = 30
BUTTON_XSIZE = settings.WINDOWWIDTH - settings.UI_MARGIN_LEFT - settings.UI_MARGIN_RIGHT
BUTTON_YSIZE = 56
BUTTON_YGAP = 6
BUTTON_TEXT_MARGIN = 4 * BUTTON_YGAP
BUTTON_READ_MARGIN = 1 * BUTTON_YGAP

BUTTON_CLEAR = 1
BUTTON_ACKNOWLEDGE = 2

BUTTONS = [
	{
		"type": "warning",
		"read": False,
		"title": "Limit Switch Hit",
		"footnote": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut mattis rutrum turpis, non faucibus diam hendrerit id. Donec non risus lacus. Pellentesque pharetra massa ac enim rutrum dignissim. Nam non pretium risus. Morbi metus sem, mattis sit amet diam sit amet, feugiat consequat arcu. Donec non nulla scelerisque, sollicitudin mauris quis, ullamcorper nibh. Proin a molestie lectus, at dignissim purus. Proin vestibulum ultrices ex, vitae sollicitudin lectus rhoncus vitae. Curabitur consequat maximus dui id tincidunt. Praesent faucibus efficitur mi non eleifend. Sed mattis varius ante, ac lacinia enim molestie in. Phasellus mollis libero in urna lacinia, sit amet viverra enim maximus",
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
		notification_color = colours.INFO_BLUE
		icon_img = "info_icn_42.png"
	elif button["type"] == "success":
		notification_color = colours.SUCCESS_GREEN
		icon_img = "success_icn_42.png"
	elif button["type"] == "warning":
		notification_color = colours.WARNING_ORANGE
		icon_img = "warning_icn_42.png"
	elif button["type"] == "error":
		notification_color = colours.ERROR_RED
		icon_img = "error_icn_42.png"
	else:
		notification_color = colours.WHITE

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

def message_display(surface, button, title_font=MESSAGE_TITLE_FONT, footnote_font= MESSAGE_FOOTNOTE_FONT, text_color=MESSAGE_TEXT_COLOUR, footnote_text_rect=MESSAGE_FOOTNOTE_RECT):
	Header(surface, "Messages", colours.WHITE)

	if button["type"] == "info":
		notification_color = colours.INFO_BLUE
		icon_img = "info_icn_63.png"
	elif button["type"] == "success":
		notification_color = colours.SUCCESS_GREEN
		icon_img = "success_icn_63.png"
	elif button["type"] == "warning":
		notification_color = colours.WARNING_ORANGE
		icon_img = "warning_icn_63.png"
	elif button["type"] == "error":
		notification_color = colours.ERROR_RED
		icon_img = "error_icn_63.png"
	else:
		notification_color = colours.WHITE

	# Image
	icn_img = pygame.image.load(icon_img).convert_alpha()
	icn_img_rect = icn_img.get_rect()
	icn_img_rect.midtop = (settings.WINDOWWIDTH/2, settings.UI_MARGIN_TOP)
	surface.blit(icn_img, icn_img_rect)

	# Header
	button_text_surf = title_font.render(button["title"], True, notification_color)
	button_text_rect = button_text_surf.get_rect()
	button_text_rect.midtop = (settings.WINDOWWIDTH/2, MESSAGE_TITLE_MARGIN_TOP)
	surface.blit(button_text_surf, button_text_rect)

	# Footnote
	DrawTextBox(surface, button["footnote"], text_color, footnote_text_rect, footnote_font, aa=True)

	# Buttons
	message_buttons = []

	# Clear

	button_rect = Rect((0,0, 145, 36))
	button_rect.topleft = (settings.UI_MARGIN, footnote_text_rect.y+ footnote_text_rect.height)
	button_rect = FilledRoundedRectangle(surface, button_rect, colours.BUTTON_2_BG_COLOR, 0.4)
	message_buttons.append({"target": button_rect, "value": BUTTON_CLEAR})

	button_text_surf = fonts.SF_UI_DISPLAY_LIGHT.render("Clear", True, colours.BUTTON_2_TEXT_COLOR)
	button_text_rect = button_text_surf.get_rect()
	button_text_rect.center = button_rect.center
	surface.blit(button_text_surf, button_text_rect)

	# Acknowledge

	button_rect = Rect((0,0, 145, 36))
	button_rect.topright = (settings.WINDOWWIDTH - settings.UI_MARGIN, footnote_text_rect.y+ footnote_text_rect.height)
	button_rect = FilledRoundedRectangle(surface, button_rect, colours.BUTTON_3_BG_COLOR, 0.4)
	message_buttons.append({"target": button_rect, "value": BUTTON_ACKNOWLEDGE})


	button_text_surf = fonts.SF_UI_DISPLAY_LIGHT.render("Acknowledge", True, colours.BUTTON_3_TEXT_COLOR)
	button_text_rect = button_text_surf.get_rect()
	button_text_rect.center = button_rect.center
	surface.blit(button_text_surf, button_text_rect)

	return message_buttons