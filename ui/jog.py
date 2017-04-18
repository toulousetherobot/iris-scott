"""
Created on April 17, 2017
@author: aramael
"""
import pygame
from pygame.locals import *

import ui.fonts
import ui.colours
from ui.utilities import FilledRoundedRectangle, FilledCircle, FillGradient

CONTROLLER_VALUE_FONT = ui.fonts.SF_UI_DISPLAY_LIGHT_XL
CONTROLLER_TAG_FONT = ui.fonts.SF_UI_TEXT_LIGHT_FOOTNOTE
CONTROLLER_CIRC_RADIUS = 36
CONTROLLER_XSIZE = ui.WINDOWWIDTH-ui.UI_MARGIN*2
CONTROLLER_YSIZE = 65
CONTROLLER_YGAP = 6

AXIS_X = 1
AXIS_Y = 2
AXIS_Z = 3

AXIS_THETA1 = 4
AXIS_THETA2 = 5

BUTTON_ADD = 1
BUTTON_ADD_ICN = "plus_icn_15.png"
BUTTON_SUBTRACT = 2
BUTTON_SUBTRACT_ICN = "minus_icn_15.png"

AXIS_CARTESIAN = [{
		"id": AXIS_X,
		"name": "X Coordinate",
		"max": 0.000,
		"min": 17.000,
		"change": 0.100,
		"color": ui.colours.PHOSPHORIC_COLORS,
	},{
		"id": AXIS_Y,
		"name": "Y Coordinate",
		"max": 0.000,
		"min": 17.000,
		"change": 0.100,
		"color": ui.colours.PINK_COLORS,
	},{
		"id": AXIS_Z,
		"name": "Z Coordinate",
		"max": 0.000,
		"min": 17.000,
		"change": 0.100,
		"color": ui.colours.CYAN_COLORS,
	}]

AXIS_JOINT = [{
		"id": AXIS_THETA1,
		"name": "Theta 1 Angle",
		"max": 0.000,
		"min": 17.000,
		"change": 0.100,
		"color": ui.colours.PHOSPHORIC_COLORS,
	},{
		"id": AXIS_THETA2,
		"name": "Theta 2 Angle",
		"max": 0.000,
		"min": 17.000,
		"change": 0.100,
		"color": ui.colours.PINK_COLORS,
	},{
		"id": AXIS_Z,
		"name": "Z Distance",
		"max": 0.000,
		"min": 17.000,
		"change": 0.100,
		"color": ui.colours.CYAN_COLORS,
	}]

def axis_controller(surface, controller, y, x=ui.UI_MARGIN, width=CONTROLLER_XSIZE, height=CONTROLLER_YSIZE,
	value_font=CONTROLLER_VALUE_FONT, tag_font=CONTROLLER_TAG_FONT, radius=CONTROLLER_CIRC_RADIUS):

	rect         = Rect((x,y,width,height))
	color        = Color("white")
	color.a      = 0
	pos          = rect.topleft
	rect.topleft = 0,0
	mask = pygame.Surface(rect.size, SRCALPHA)
	gradient = pygame.Surface(rect.size, SRCALPHA)

	FillGradient(gradient, controller["color"][0], controller["color"][1])

	# Decrement Button
	FilledCircle(mask, (radius/2, height/2, radius), color)
	img_splash = pygame.image.load(BUTTON_SUBTRACT_ICN).convert_alpha()
	img_splash_rect = img_splash.get_rect()
	mask.blit(img_splash, (radius/2-img_splash_rect.width/2, height/2-img_splash_rect.height/2))

	# Increment Button
	FilledCircle(mask, (width-radius/2, height/2, radius), color)
	img_splash = pygame.image.load(BUTTON_ADD_ICN).convert_alpha()
	img_splash_rect = img_splash.get_rect()
	mask.blit(img_splash, (width-radius/2-img_splash_rect.width/2, height/2-img_splash_rect.height/2))

	# Value
	button_text_surf = value_font.render("11.246", True, color)
	button_text_rect = button_text_surf.get_rect()
	button_text_rect.midtop = (width/2, -15)
	mask.blit(button_text_surf, button_text_rect)

	# Name
	button_text_surf = tag_font.render(controller["name"], True, color)
	button_text_rect = button_text_surf.get_rect()
	button_text_rect.midbottom = (width/2, height)
	mask.blit(button_text_surf, button_text_rect)

	gradient.blit(mask, (0, 0), None, BLEND_RGBA_MULT)
	surface.blit(gradient, pos)

	# return {"target": button_rect, "value": controller["id"]}