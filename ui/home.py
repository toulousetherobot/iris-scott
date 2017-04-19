"""
Created on April 17, 2017
@author: aramael
"""
import pygame
from pygame.locals import *
from copy import deepcopy

from . import settings
from . import fonts
from . import colours

from ui.utilities import FillGradient

GLANCE_VALUE_FONT = fonts.SF_UI_DISPLAY_LIGHT_XL
GLANCE_ID_FONT = fonts.SF_UI_TEXT_LIGHT_HEADER
GLANCE_XSIZE = settings.WINDOWWIDTH - settings.UI_MARGIN_LEFT - settings.UI_MARGIN_RIGHT
GLANCE_YSIZE = 48
GLANCE_YGAP = 4

GLANCES = [{
		"identifier": "frame",
		"label": "FRM",
		"color": colours.WHITE,
	},{
		"identifier": "X",
		"label": "X",
		"color": colours.PHOSPHORIC_COLORS,
	},{
		"identifier": "Y",
		"label": "Y",
		"color": colours.PINK_COLORS,
	},{
		"identifier": "Z",
		"label": "Z",
		"color": colours.CYAN_COLORS,
	}]

def glance(surface, robot, glance, y, x=settings.UI_MARGIN, width=GLANCE_XSIZE, height=GLANCE_YSIZE,
	value_font=GLANCE_VALUE_FONT, identifier_font=GLANCE_ID_FONT):

	if (glance["identifier"] == "frame" and robot.program is None):
		return

	rect         = Rect((x,y,width,height))
	original_color = deepcopy(glance["color"])
	if isinstance(glance["color"], list):
		color        = Color("white")
	else: 
		color        = Color(*glance["color"])
	color.a      = 0
	pos          = rect.topleft
	rect.topleft = 0,0
	mask = pygame.Surface(rect.size, SRCALPHA)
	gradient = pygame.Surface(rect.size, SRCALPHA)

	# Value
	if (glance["identifier"] == "frame"):
		text = "{:d}/{:d}".format(getattr(robot, glance["identifier"], 0), getattr(robot, "total_frames", 0))
	else:
		text = "{:05.3f}".format(getattr(robot, glance["identifier"], 0.000))
	text_surf = value_font.render(text, True, color)
	value_text_rect = text_surf.get_rect()
	value_text_rect.topleft = (x, -15)
	mask.blit(text_surf, value_text_rect)

	# Name
	text_surf = identifier_font.render(glance["label"], True, color)
	id_text_rect = text_surf.get_rect()
	id_text_rect.bottomleft = (value_text_rect.right, value_text_rect.bottom-10)
	mask.blit(text_surf, id_text_rect)


    # Mask Gradient with Rounded
	if isinstance(original_color, list):
		FillGradient(gradient, glance["color"][0], glance["color"][1])
		gradient.blit(mask, (0, 0), None, BLEND_RGBA_MULT)
		surface.blit(gradient, pos)
	else:
		surface.blit(mask, pos)