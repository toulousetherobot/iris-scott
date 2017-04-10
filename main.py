'''
Created on April 9, 2017
@author: aramael
'''
import pygame
import sys
from pygame.locals import *
from datetime import datetime, timedelta

# UI Constants & Helper Functions
from ui.passcode import *
from ui.fonts import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 320 # size of window's width in pixels
WINDOWHEIGHT = 240 # size of windows' height in pixels

#            R    G    B
BLACK    = (  0,   0,   0)
WHITE    = (255, 255, 255)

BGCOLOR = BLACK

# Windows
UI_WIN_SPLASH_SCREEN = 1
UI_WIN_PASSCODE_LOCK_SCREEN = 2
UI_WIN_HOME_SCREEN = 3
UI_WIN_MAIN_MENU_SCREEN = 4
UI_WIN_MANUAL_JOG_CARTESIAN_SCREEN = 5
UI_WIN_MANUAL_JOG_JOINT_SCREEN = 6
UI_WIN_PROGRAM_SELECTION_SCREEN = 7
UI_WIN_PHOTO_CAPTURE_SCREEN = 8
UI_WIN_CURVES_SELECTION_SCREEN = 9
UI_WIN_MESSAGES_LIST_SCREEN = 10
UI_WIN_MESSAGE_INFO_SCREEN = 11
UI_WIN_MESSAGE_SUCCESS_SCREEN = 12
UI_WIN_MESSAGE_WARNING_SCREEN = 13
UI_WIN_MESSAGE_ERROR_SCREEN = 14


def main():
  global FPSCLOCK, DISPLAYSURF
  pygame.init()
  FPSCLOCK = pygame.time.Clock()
  
  # Screen Size
  DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
  DISPLAYSURF.fill(BGCOLOR)
  # os.putenv('SDL_FBDEV', '/dev/fb1')

  mousex = 0 # used to store x coordinate of mouse event
  mousey = 0 # used to store y coordinate of mouse event
  pygame.display.set_caption('Toulouse')

  # Start Up with Splash Screen
  os_state = UI_WIN_SPLASH_SCREEN
  loaded_new_state = 0

  # Image Loading
  img_splash = pygame.image.load('splash.png').convert_alpha()
  SPLASH_TIMEOUT = 1
  splash_start = datetime.now() + timedelta(seconds=SPLASH_TIMEOUT)

  # Passcode Peristent Variables
  passcode = [1, 9, 0, 1]
  passcode_attempt = []
  passcode_failed_attempts = 0

  while True:
    mouseClicked = False

    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == MOUSEBUTTONDOWN:
        mousex, mousey = event.pos
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)
      elif event.type == MOUSEMOTION:
        mousex, mousey = event.pos
        pygame.event.clear(pygame.MOUSEMOTION)
      elif event.type == MOUSEBUTTONUP:
        mousex, mousey = event.pos
        mouseClicked = True
        pygame.event.clear(pygame.MOUSEBUTTONUP)

    # Window Tree
    if (os_state == UI_WIN_SPLASH_SCREEN):
      if (not loaded_new_state):
        print("----> Displaying Splash Screen")
        splash_start = datetime.now() + timedelta(seconds=SPLASH_TIMEOUT)
        loaded_new_state = 1
        DISPLAYSURF.fill(BGCOLOR)

      DISPLAYSURF.blit(img_splash, (20, 59))

      # Timer to Passcode Lock
      if (datetime.now() > splash_start):
        os_state = UI_WIN_PASSCODE_LOCK_SCREEN
        loaded_new_state = 0
    elif (os_state == UI_WIN_PASSCODE_LOCK_SCREEN):
      if (not loaded_new_state):
        print("----> Displaying Passcode Lock Screen")
        loaded_new_state = 1
        DISPLAYSURF.fill(BGCOLOR) # Reset Frame

        passcode_title = "Enter Passcode"

        # Draw Buttons Once
        passcode_buttons = []
        buttonx, buttony = PASSCODE_BUTTON_XSTART, PASSCODE_BUTTON_YSTART
        for row in PASSCODE_BUTTON_STRUCTURE:
          if len(row) == 3:
            for column in row:
              if column is not None:
                passcode_buttons.append(rounded_button(DISPLAYSURF, column, buttonx, buttony))
              buttonx += PASSCODE_BUTTON_XSIZE + PASSCODE_BUTTON_XGAP
            buttony += PASSCODE_BUTTON_YSIZE + PASSCODE_BUTTON_YGAP
          elif len(row) == 1:
            passcode_buttons.append(rounded_button(DISPLAYSURF, row[0], buttonx, buttony, width=PASSCODE_BUTTON_XSIZE*3+PASSCODE_BUTTON_XGAP*2))
          buttonx = PASSCODE_BUTTON_XSTART

      # Update Passcode Entry
      if (len(passcode_attempt) > 0):
        # display only most recent digit
        passcode_title = (u"\u2022 " * (len(passcode_attempt)-1))
        passcode_title += str(passcode_attempt[-1])
      elif(len(passcode_attempt) == 0):
        passcode_title = "Enter Passcode"

      # Render Passcode Header
      passcode_text_blackout_rect = pygame.Rect(0, 0, WINDOWWIDTH, PASSCODE_BUTTON_YSTART)
      pygame.draw.rect(DISPLAYSURF, BGCOLOR, passcode_text_blackout_rect)
      passcode_text_surf = SF_UI_DISPLAY_HEAVY.render(passcode_title, True, WHITE, BLACK)
      passcode_text_rect = passcode_text_surf.get_rect()
      passcode_text_rect.center = (WINDOWWIDTH/2, PASSCODE_BUTTON_YSTART/2)
      DISPLAYSURF.blit(passcode_text_surf, passcode_text_rect)

      # Button Logic
      if (mouseClicked):
        for button in passcode_buttons:
          if button["target"].collidepoint((mousex, mousey)):
            if (button["value"].isdigit()):
              passcode_attempt.append(int(button["value"]))
            elif (button["value"] == "<"):
              passcode_attempt.pop()
            elif (button["value"] == "clear"):
              del passcode_attempt[:]
            print("Passcode Attempt: ", passcode_attempt)
            print("Clicked", button["value"])

      if (len(passcode_attempt) >= len(passcode)):
        # Passcode Entered Successfully
        if (passcode_attempt == passcode):
          passcode_failed_attempts = 0
          os_state = UI_WIN_HOME_SCREEN
          loaded_new_state = 0
        else:
          passcode_failed_attempts += 1
          print("Failed Attempts: ", passcode_failed_attempts)
          passcode_title = "Wrong Passcode"
        del passcode_attempt[:]
    elif (os_state == UI_WIN_MAIN_MENU_SCREEN):
      if (not loaded_new_state):
        print("----> Displaying Main Menu Screen")
        loaded_new_state = 1
        DISPLAYSURF.fill(BGCOLOR)
    elif (os_state == UI_WIN_MANUAL_JOG_CARTESIAN_SCREEN):
      if (not loaded_new_state):
        print("----> Displaying Manual Jog (Cartesian) Screen")
        loaded_new_state = 1
        DISPLAYSURF.fill(BGCOLOR)
    elif (os_state == UI_WIN_MANUAL_JOG_JOINT_SCREEN):
      if (not loaded_new_state):
        print("----> Displaying Manual Jog (Joint Angles) Screen")
        loaded_new_state = 1
        DISPLAYSURF.fill(BGCOLOR)
    elif (os_state == UI_WIN_PROGRAM_SELECTION_SCREEN):
      if (not loaded_new_state):
        print("----> Displaying Program Selection Screen")
        loaded_new_state = 1
        DISPLAYSURF.fill(BGCOLOR)
    elif (os_state == UI_WIN_PHOTO_CAPTURE_SCREEN):
      if (not loaded_new_state):
        print("----> Displaying Photo Capture Screen")
        loaded_new_state = 1
        DISPLAYSURF.fill(BGCOLOR)
    elif (os_state == UI_WIN_CURVES_SELECTION_SCREEN):
      if (not loaded_new_state):
        print("----> Displaying Curves Selection Screen")
        loaded_new_state = 1
        DISPLAYSURF.fill(BGCOLOR)
    elif (os_state == UI_WIN_MESSAGES_LIST_SCREEN):
      if (not loaded_new_state):
        print("----> Displaying Message List Screen")
        loaded_new_state = 1
        DISPLAYSURF.fill(BGCOLOR)
    elif (os_state == UI_WIN_MESSAGE_INFO_SCREEN):
      if (not loaded_new_state):
        print("----> Displaying Message (Info) Screen")
        loaded_new_state = 1
        DISPLAYSURF.fill(BGCOLOR)
    elif (os_state == UI_WIN_MESSAGE_SUCCESS_SCREEN):
      if (not loaded_new_state):
        print("----> Displaying Message (Success) Screen")
        loaded_new_state = 1
        DISPLAYSURF.fill(BGCOLOR)
    elif (os_state == UI_WIN_MESSAGE_WARNING_SCREEN):
      if (not loaded_new_state):
        print("----> Displaying Message (Warning) Screen")
        loaded_new_state = 1
        DISPLAYSURF.fill(BGCOLOR)
    elif (os_state == UI_WIN_MESSAGE_ERROR_SCREEN):
      if (not loaded_new_state):
        print("----> Displaying Message (Error) Screen")
        loaded_new_state = 1
        DISPLAYSURF.fill(BGCOLOR)
    else: # Display Home Screen
      if (not loaded_new_state):
        print("----> Displaying Home Screen")
        loaded_new_state = 1
        DISPLAYSURF.fill(BGCOLOR)

    # Redraw the screen and wait a clock tick.
    pygame.display.update()
    FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()