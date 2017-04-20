"""
Created on April 17, 2017
@author: aramael
"""
import pygame
from pygame.locals import *

from . import settings
from . import fonts
from . import colours

from ui.utilities import FilledRoundedRectangle, FilledCircle, FillGradient

CONTROLLER_VALUE_FONT = fonts.SF_UI_DISPLAY_LIGHT_XL
CONTROLLER_TAG_FONT = fonts.SF_UI_TEXT_LIGHT_FOOTNOTE
CONTROLLER_CIRC_RADIUS = 36
CONTROLLER_XSIZE = settings.WINDOWWIDTH - settings.UI_MARGIN_LEFT - settings.UI_MARGIN_RIGHT
CONTROLLER_YSIZE = 65
CONTROLLER_YGAP = 6

AXIS_X = 1
AXIS_Y = 2
AXIS_Z = 3

AXIS_THETA1 = 4
AXIS_THETA2 = 5
AXIS_D3     = 6

BUTTON_EDIT = 0
BUTTON_ADD = 1
BUTTON_ADD_ICN = "plus_icn_15.png"
BUTTON_SUBTRACT = 2
BUTTON_SUBTRACT_ICN = "minus_icn_15.png"

AXIS_CARTESIAN = [{
		"id": AXIS_X,
		"identifier": "X",
		"name": "X Coordinate",
		"max": 0.000,
		"min": 17.000,
		"change": 0.100,
		"color": colours.PHOSPHORIC_COLORS,
	},{
		"id": AXIS_Y,
		"identifier": "Y",
		"name": "Y Coordinate",
		"max": 0.000,
		"min": 17.000,
		"change": 0.100,
		"color": colours.PINK_COLORS,
	},{
		"id": AXIS_Z,
		"identifier": "Z",
		"name": "Z Coordinate",
		"max": 0.000,
		"min": 17.000,
		"change": 0.100,
		"color": colours.CYAN_COLORS,
	}]

AXIS_JOINT = [{
		"id": AXIS_THETA1,
		"name": "Theta 1 Angle",
		"max": 0.000,
		"min": 17.000,
		"change": 0.100,
		"color": colours.PHOSPHORIC_COLORS,
	},{
		"id": AXIS_THETA2,
		"name": "Theta 2 Angle",
		"max": 0.000,
		"min": 17.000,
		"change": 0.100,
		"color": colours.PINK_COLORS,
	},{
		"id": AXIS_D3,
		"name": "Z Distance",
		"max": 0.000,
		"min": 17.000,
		"change": 0.100,
		"color": colours.CYAN_COLORS,
	}]

def axis_controller(surface, robot, controller, y, x=settings.UI_MARGIN, width=CONTROLLER_XSIZE, height=CONTROLLER_YSIZE,
	value_font=CONTROLLER_VALUE_FONT, tag_font=CONTROLLER_TAG_FONT, radius=CONTROLLER_CIRC_RADIUS):

	rect         = Rect((x,y,width,height))
	color        = Color("white")
	color.a      = 0
	pos          = rect.topleft
	rect.topleft = 0,0
	mask = pygame.Surface(rect.size, SRCALPHA)
	gradient = pygame.Surface(rect.size, SRCALPHA)

	FillGradient(gradient, controller["color"][0], controller["color"][1])

	buttons = []

	# Decrement Button
	button_rect = FilledCircle(mask, (radius/2, height/2, radius), color)
	img_splash = pygame.image.load(BUTTON_SUBTRACT_ICN).convert_alpha()
	img_splash_rect = img_splash.get_rect()
	mask.blit(img_splash, (radius/2-img_splash_rect.width/2, height/2-img_splash_rect.height/2))
	button_rect.topleft = (button_rect.x + pos[0], button_rect.y + pos[1]) # Modify Rect for Final Placement
	buttons.append({"target": button_rect, "value": BUTTON_SUBTRACT, "action": controller["identifier"], "change": controller["change"]})

	# Increment Button
	button_rect = FilledCircle(mask, (width-radius/2, height/2, radius), color)
	img_splash = pygame.image.load(BUTTON_ADD_ICN).convert_alpha()
	img_splash_rect = img_splash.get_rect()
	mask.blit(img_splash, (width-radius/2-img_splash_rect.width/2, height/2-img_splash_rect.height/2))
	button_rect.topleft = (button_rect.x + pos[0], button_rect.y + pos[1]) # Modify Rect for Final Placement
	buttons.append({"target": button_rect, "value": BUTTON_ADD, "action": controller["identifier"], "change": controller["change"]})

	# Value
	text = "{:05.3f}".format(getattr(robot, controller["identifier"], 0.000))
	text_surf = value_font.render(text, True, color)
	text_rect = text_surf.get_rect()
	text_rect.midtop = (width/2, -15)
	mask.blit(text_surf, text_rect)
	text_rect.topleft = (text_rect.x + pos[0], text_rect.y + pos[1]) # Modify Rect for Final Placement
	buttons.append({"target": text_rect, "value": BUTTON_EDIT, "action": controller["identifier"]})

	# Name
	text_surf = tag_font.render(controller["name"], True, color)
	text_rect = text_surf.get_rect()
	text_rect.midbottom = (width/2, height)
	mask.blit(text_surf, text_rect)

	gradient.blit(mask, (0, 0), None, BLEND_RGBA_MULT)
	surface.blit(gradient, pos)

	return buttons