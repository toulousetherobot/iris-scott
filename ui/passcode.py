"""
Created on April 9, 2017
@author: aramael
"""
import pygame
from pygame.locals import *

import ui.fonts

# Passcode Lock Screen
PASSCODE_BUTTON_TEXT_COLOR = (255, 255, 255)
PASSCODE_BUTTON_BG_COLOR = (79, 79, 79)
PASSCODE_BUTTON_YSTART = 30
PASSCODE_BUTTON_XSTART = 30
PASSCODE_BUTTON_XSIZE = 80
PASSCODE_BUTTON_YSIZE = 36
PASSCODE_BUTTON_XGAP = 8
PASSCODE_BUTTON_YGAP = 4
PASSCODE_BUTTON_STRUCTURE = [["1","2","3"],["4","5","6"],["7","8","9"],[None,"0","<"],["clear"]]

def rounded_button(surface, text, x, y, font=ui.fonts.SF_UI_DISPLAY_HEAVY, width=PASSCODE_BUTTON_XSIZE, height=PASSCODE_BUTTON_YSIZE, text_color=PASSCODE_BUTTON_TEXT_COLOR, backround_color=PASSCODE_BUTTON_BG_COLOR):
  button_rect = pygame.Rect(x, y, width, height)
  pygame.draw.rect(surface, backround_color, button_rect)
  button_text_surf = font.render(text, True, text_color)
  button_text_rect = button_text_surf.get_rect()
  button_text_rect.center = (x + width/2, y + height/2)
  surface.blit(button_text_surf, button_text_rect)

  return {"target": button_rect, "value": text}