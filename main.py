'''
Created on April 9, 2017
@author: aramael
'''
import pygame
import sys
import os
import stat
from pygame.locals import *
from datetime import datetime, timedelta

# UI Constants & Helper Functions
import ui
from ui.passcode import *

def main():

  PITFT_BUTTON_1 = 23
  PITFT_BUTTON_2 = 22
  PITFT_BUTTON_3 = 17
  PITFT_BUTTON_4 = 27

  running_on_pi = False

  #
  # Camera Params
  #
  sizeData = [ # Camera parameters for different size settings
  # Full res      Viewfinder  Crop window
  [(2592, 1944), (320, 240), (0.0   , 0.0   , 0.0   , 0.0   )]] # Large

  sizeMode = 0

  # Buffers for viewfinder data
  rgb = bytearray(int(ui.settings.WINDOWWIDTH * ui.settings.WINDOWHEIGHT * 3))
  yuv = bytearray(int(ui.settings.WINDOWWIDTH * ui.settings.WINDOWHEIGHT * 3 / 2))

  if (os.getenv('FRAMEBUFFER') is not None):
    print ("RUNNING ON PI")
    running_on_pi = True
    # Pi Specific Settings
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.putenv('SDL_FBDEV', '/dev/fb1')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
    os.putenv('SDL_MOUSEDRV', 'TSLIB')

    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    for k in [PITFT_BUTTON_1, PITFT_BUTTON_2, PITFT_BUTTON_3, PITFT_BUTTON_4]:
        GPIO.setup(k, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    import io
    import picamera
    import yuv2rgb

    # Init camera and set up default values
    camera = picamera.PiCamera()
    camera.resolution = sizeData[sizeMode][1]
    camera.crop = sizeData[sizeMode][2]
    # Leave raw format at default YUV, don't touch, don't set to RGB!

  global FPSCLOCK, DISPLAYSURF
  pygame.init()
  FPSCLOCK = pygame.time.Clock()
  
  # Screen Size
  DISPLAYSURF = pygame.display.set_mode((settings.WINDOWWIDTH, settings.WINDOWHEIGHT))

  mousex = 0 # used to store x coordinate of mouse event
  mousey = 0 # used to store y coordinate of mouse event

  if (running_on_pi):
    pygame.mouse.set_visible(False)
  else:
    pygame.display.set_caption('Toulouse')

  # Initalise OS Logic State
  toulouse = ui.state.Toulouse(running_on_pi)
  toulouse.locked = False
  toulouse.load()
  toulouse.load_screen(ui.state.Page.PHOTO_CAPTURE_SCREEN)

  # Security
  passcode_attempt = []

  # Message Display
  message_id = None

  # Image Loading
  SPLASH_TIMEOUT = 1
  splash_start = None

  # Caricature Paramaters
  cusd_queue_id = None
  cusd_queue_id = "nSsRGBCj"

  # Scroll Parameters
  scroll_y_min = 0
  scroll_y = 0
  scroll_y_max = 0

  while True:

    if (toulouse.mode != ui.state.Mode.UNINITIALIZED_MODE):
      toulouse.check_messages()

    if (toulouse.locked and toulouse.page != ui.state.Page.SPLASH_SCREEN):
      toulouse.load_screen(ui.state.Page.PASSCODE_LOCK_SCREEN)

    mouseClicked = False

    if (running_on_pi):
      # Button #1 (Mocked by Q) Back
      # if (not toulouse.locked and GPIO.input(PITFT_BUTTON_1) == False):
      #   toulouse.back()

      # Button #2 (Mocked by W) Messages
      if (not toulouse.locked and GPIO.input(PITFT_BUTTON_2) == False):
        toulouse.load_screen(ui.state.Page.MESSAGES_LIST_SCREEN)

      # Button #3 (Mocked by E) Program Selection
      if (not toulouse.locked and GPIO.input(PITFT_BUTTON_3) == False):
        toulouse.load_screen(ui.state.Page.PROGRAM_SELECTION_SCREEN)

      # Button #4 (Mocked by R) Main Menu
      if (not toulouse.locked and GPIO.input(PITFT_BUTTON_4) == False):
        toulouse.load_screen(ui.state.Page.MAIN_MENU_SCREEN)

    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == MOUSEBUTTONDOWN:
        mousex, mousey = event.pos
        if event.button == 4: scroll_y = min(scroll_y + 15, scroll_y_min)
        if event.button == 5: scroll_y = max(scroll_y - 15, scroll_y_max)
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)
      elif event.type == MOUSEMOTION:
        mousex, mousey = event.pos
        pygame.event.clear(pygame.MOUSEMOTION)
      elif event.type == MOUSEBUTTONUP:
        mousex, mousey = event.pos
        if (event.button != 4 and event.button != 5):
          mouseClicked = True
        pygame.event.clear(pygame.MOUSEBUTTONUP)
      elif event.type == pygame.KEYDOWN:
        # Button #1 (Mocked by Q) Back
        if (not toulouse.locked and event.key == pygame.K_q):
          toulouse.back()

        # Button #2 (Mocked by W) Messages
        if (not toulouse.locked and event.key == pygame.K_w):
          toulouse.load_screen(ui.state.Page.MESSAGES_LIST_SCREEN)

        # Button #3 (Mocked by E) Program Selection
        if (not toulouse.locked and event.key == pygame.K_e):
          toulouse.load_screen(ui.state.Page.PROGRAM_SELECTION_SCREEN)

        # Button #4 (Mocked by R) Main Menu
        if (not toulouse.locked and event.key == pygame.K_r):
          toulouse.load_screen(ui.state.Page.MAIN_MENU_SCREEN)

    # Window Tree
    if (toulouse.page == ui.state.Page.SPLASH_SCREEN):
      if (not toulouse.loaded_new_state):
        print("----> Displaying Splash Screen")
        splash_start = datetime.now() + timedelta(seconds=SPLASH_TIMEOUT)
        DISPLAYSURF.fill(ui.colours.SCREEN_BG_COLOR)
        img_splash_surf = pygame.image.load('/home/pi/toulouseos/splash.png').convert_alpha()
        img_splash_rect = img_splash_surf.get_rect()
        img_splash_rect.center = (settings.WINDOWWIDTH/2, settings.WINDOWHEIGHT/2)
        DISPLAYSURF.blit(img_splash_surf, img_splash_rect)

        inetaddr_text_surf = ui.fonts.SF_UI_DISPLAY_HEAVY.render(toulouse.inetaddr, True, ui.colours.WHITE, ui.colours.BLACK)
        inetaddr_text_rect = inetaddr_text_surf.get_rect()
        inetaddr_text_rect.midtop = (settings.WINDOWWIDTH/2, settings.WINDOWHEIGHT-settings.UI_MARGIN_TOP)
        DISPLAYSURF.blit(inetaddr_text_surf, inetaddr_text_rect)

        toulouse.load()
        toulouse.loaded_screen(ui.state.Page.SPLASH_SCREEN)

      # Timer to Passcode Lock
      if (datetime.now() > splash_start):
        toulouse.load_screen(ui.state.Page.PASSCODE_LOCK_SCREEN)
    elif (toulouse.page == ui.state.Page.PASSCODE_LOCK_SCREEN):
      if (not toulouse.loaded_new_state):
        print("----> Displaying Passcode Lock Screen")
        DISPLAYSURF.fill(ui.colours.SCREEN_BG_COLOR) # Reset Frame

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
        toulouse.loaded_screen(ui.state.Page.PASSCODE_LOCK_SCREEN)

      # Update Passcode Entry
      if (len(passcode_attempt) > 0):
        # display only most recent digit
        passcode_title = (u"\u2022 " * (len(passcode_attempt)-1))
        passcode_title += str(passcode_attempt[-1])
      elif(len(passcode_attempt) == 0 and passcode_title != "Wrong Passcode"):
        passcode_title = "Enter Passcode"

      # Render Passcode Header
      passcode_text_blackout_rect = pygame.Rect(0, 0, settings.WINDOWWIDTH, settings.UI_MARGIN_TOP)
      pygame.draw.rect(DISPLAYSURF, ui.colours.SCREEN_BG_COLOR, passcode_text_blackout_rect)
      passcode_text_surf = ui.fonts.SF_UI_DISPLAY_HEAVY.render(passcode_title, True, ui.colours.WHITE, ui.colours.BLACK)
      passcode_text_rect = passcode_text_surf.get_rect()
      passcode_text_rect.center = (settings.WINDOWWIDTH/2, settings.UI_MARGIN_TOP/2)
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

      # Attempt to Login
      login_attempt = toulouse.login(passcode_attempt)
      if (login_attempt == False):
        passcode_title = "Wrong Passcode"
        del passcode_attempt[:]
      elif (login_attempt == True):
        del passcode_attempt[:]
    elif (toulouse.page == ui.state.Page.MAIN_MENU_SCREEN):
      if (not toulouse.loaded_new_state):
        print("----> Displaying Main Menu Screen")
        DISPLAYSURF.fill(ui.colours.SCREEN_BG_COLOR)

        # Draw Buttons Once
        menu_buttons = []

        cancel_text_surf = ui.fonts.SF_UI_DISPLAY_HEAVY.render("Cancel", True, ui.colours.WHITE, ui.colours.BLACK)
        cancel_text_rect = cancel_text_surf.get_rect()
        cancel_text_rect.midleft = (settings.UI_MARGIN, settings.UI_MARGIN_TOP/2)
        DISPLAYSURF.blit(cancel_text_surf, cancel_text_rect)
        menu_buttons.append({"target": cancel_text_rect, "value": 4})

        for i in range(len(ui.mainmenu.BUTTONS)):
          menu_buttons.append(ui.mainmenu.rounded_button(DISPLAYSURF, ui.mainmenu.BUTTONS[i], 
            settings.UI_MARGIN, settings.WINDOWHEIGHT-settings.UI_MARGIN_BOTTOM-(ui.mainmenu.BUTTON_YSIZE+ui.mainmenu.BUTTON_YGAP)*(i+1)))

        toulouse.loaded_screen(ui.state.Page.MAIN_MENU_SCREEN)

      # Button Logic
      if (mouseClicked):
        for button in menu_buttons:
          if button["target"].collidepoint((mousex, mousey)):
            if (button["value"] == ui.mainmenu.BUTTON_SHUTDOWN):
              toulouse.shutdown()
            if (button["value"] == ui.mainmenu.BUTTON_RESTART):
              toulouse.restart()
            if (button["value"] == ui.mainmenu.BUTTON_LOCK):
              toulouse.lock()
            if (button["value"] == ui.mainmenu.BUTTON_CANCEL):
              toulouse.back()
    elif (toulouse.page == ui.state.Page.MANUAL_JOG_CARTESIAN_SCREEN):
      if (not toulouse.loaded_new_state):
        print("----> Displaying Manual Jog (Cartesian) Screen")
        
        toulouse.loaded_screen(ui.state.Page.MANUAL_JOG_CARTESIAN_SCREEN)

      DISPLAYSURF.fill(ui.colours.SCREEN_BG_COLOR)

      axis_buttons = []

      axis_buttons.append(ui.utilities.Header(DISPLAYSURF, toulouse, "Cartesian Jog", ui.colours.WHITE))

      for i in range(len(ui.jog.AXIS_CARTESIAN)):
        axis_buttons.extend(ui.jog.axis_controller(DISPLAYSURF, toulouse, ui.jog.AXIS_CARTESIAN[i], settings.UI_MARGIN_TOP+(ui.jog.CONTROLLER_YSIZE+ui.jog.CONTROLLER_YGAP)*i))

      if (mouseClicked):
        for button in axis_buttons:
          if button["target"].collidepoint((mousex, mousey)):
            if button["value"] == ui.utilities.BUTTON_HEADER:
              toulouse.load_screen(ui.state.Page.MANUAL_JOG_JOINT_SCREEN)
              break
            curr_value = getattr(toulouse, button["action"], 0.00)
            if button["value"] == ui.jog.BUTTON_EDIT:
              pass
            elif button["value"] == ui.jog.BUTTON_ADD:
              setattr(toulouse, button["action"], curr_value + button["change"])
            elif button["value"] == ui.jog.BUTTON_SUBTRACT:
              setattr(toulouse, button["action"], curr_value - button["change"])
    elif (toulouse.page == ui.state.Page.MANUAL_JOG_JOINT_SCREEN):
      if (not toulouse.loaded_new_state):
        print("----> Displaying Manual Jog (Joint Angles) Screen")
        toulouse.loaded_screen(ui.state.Page.MANUAL_JOG_JOINT_SCREEN)

      DISPLAYSURF.fill(ui.colours.SCREEN_BG_COLOR)
      axis_buttons = []

      axis_buttons.append(ui.utilities.Header(DISPLAYSURF, toulouse, "Joint Jog", ui.colours.WHITE))

      for i in range(len(ui.jog.AXIS_JOINT)):
        axis_buttons.extend(ui.jog.axis_controller(DISPLAYSURF, toulouse, ui.jog.AXIS_JOINT[i], settings.UI_MARGIN_TOP+(ui.jog.CONTROLLER_YSIZE+ui.jog.CONTROLLER_YGAP)*i))

      if (mouseClicked):
        for button in axis_buttons:
          if button["target"].collidepoint((mousex, mousey)):
            if button["value"] == ui.utilities.BUTTON_HEADER:
              toulouse.load_screen(ui.state.Page.MANUAL_JOG_CARTESIAN_SCREEN)
              break
            curr_value = getattr(toulouse, button["action"], 0.00)
            if button["value"] == ui.jog.BUTTON_EDIT:
              pass
            elif button["value"] == ui.jog.BUTTON_ADD:
              setattr(toulouse, button["action"], curr_value + button["change"])
            elif button["value"] == ui.jog.BUTTON_SUBTRACT:
              setattr(toulouse, button["action"], curr_value - button["change"])
    elif (toulouse.page == ui.state.Page.PROGRAM_SELECTION_SCREEN):
      if (not toulouse.loaded_new_state):
        print("----> Displaying Program Selection Screen")
        loaded_new_state = 1
        DISPLAYSURF.fill(ui.colours.SCREEN_BG_COLOR)

        # Draw Buttons Once
        program_buttons = []

        ui.utilities.Header(DISPLAYSURF, toulouse, "Programs", ui.colours.PHOSPHORIC_LIGHT_COLOR)

        for i in range(len(ui.program.BUTTONS)):
          program_buttons.append(ui.program.rounded_button(DISPLAYSURF, ui.program.BUTTONS[i], 
            settings.UI_MARGIN, settings.UI_MARGIN_TOP + (ui.program.BUTTON_YSIZE+ui.program.BUTTON_YGAP)*i))
        toulouse.loaded_screen(ui.state.Page.PROGRAM_SELECTION_SCREEN)

      # Button Logic
      if (mouseClicked):
        for button in program_buttons:
          if button["target"].collidepoint((mousex, mousey)):
            if (button["value"] == ui.program.BUTTON_CARICATURE):
              toulouse.load_screen(ui.state.Page.PHOTO_CAPTURE_SCREEN)
            if (button["value"] == ui.program.BUTTON_CURVES):
              toulouse.load_screen(ui.state.Page.CURVES_SELECTION_SCREEN)
    elif (toulouse.page == ui.state.Page.PHOTO_CAPTURE_SCREEN):
      if (not toulouse.loaded_new_state):
        print("----> Displaying Photo Capture Screen")
        BUTTON_PHOTO_CAPTURE = 1
        BUTTON_CUSD_CLEAR = 2
        toulouse.loaded_screen(ui.state.Page.PHOTO_CAPTURE_SCREEN)

      photo_capture_buttons = []
      # Refresh display
      stream = io.BytesIO() # Capture into in-memory stream
      camera.capture(stream, use_video_port=True, format='raw')
      stream.seek(0)
      stream.readinto(yuv)  # stream -> YUV buffer
      stream.close()
      yuv2rgb.convert(yuv, rgb, sizeData[sizeMode][1][0], sizeData[sizeMode][1][1])
      img = pygame.image.frombuffer(rgb[0:(sizeData[sizeMode][1][0] * sizeData[sizeMode][1][1] * 3)],sizeData[sizeMode][1], 'RGB')

      DISPLAYSURF.blit(img,((ui.settings.WINDOWWIDTH - img.get_width() ) / 2,(ui.settings.WINDOWHEIGHT - img.get_height()) / 2))

      ui.utilities.Header(DISPLAYSURF, toulouse, "Programs", transparency=True)

      ui.utilities.TransparentRect(DISPLAYSURF, (0,ui.settings.WINDOWHEIGHT-ui.settings.UI_MARGIN_BOTTOM - 56 - ui.settings.UI_MARGIN, ui.settings.WINDOWWIDTH, 56 + ui.settings.UI_MARGIN + ui.settings.UI_MARGIN_BOTTOM), ui.colours.SCREEN_BG_COLOR)
      button_circ = [ui.settings.WINDOWWIDTH/2, ui.settings.WINDOWHEIGHT-ui.settings.UI_MARGIN_BOTTOM - 28, 56]
      camera_capture = ui.utilities.FilledCircle(DISPLAYSURF, button_circ, ui.colours.WHITE)
      photo_capture_buttons.append({"target": camera_capture, "value": BUTTON_PHOTO_CAPTURE})
      button_circ[2] = 42
      ui.utilities.FilledCircle(DISPLAYSURF, button_circ, ui.colours.SCREEN_BG_COLOR)
      button_circ[2] = 38
      ui.utilities.FilledCircle(DISPLAYSURF, button_circ, ui.colours.WHITE)

      if (cusd_queue_id is not None):
        queue_id_text_surf = ui.fonts.OCRA.render("CUSD:{id}".format(id=cusd_queue_id), True, ui.colours.WARNING_ORANGE)
        queue_id_text_rect = queue_id_text_surf.get_rect()
        queue_id_text_rect.bottomleft = (settings.UI_MARGIN_LEFT, ui.settings.WINDOWHEIGHT-ui.settings.UI_MARGIN_BOTTOM)
        DISPLAYSURF.blit(queue_id_text_surf, queue_id_text_rect)
        photo_capture_buttons.append({"target": queue_id_text_rect, "value": BUTTON_CUSD_CLEAR})

      if (running_on_pi):
        # Button #1 (Mocked by Q) Back
        if (not toulouse.locked and GPIO.input(PITFT_BUTTON_1) == False):
          toulouse.process_caricature(camera)

      # Button Logic
      # if (mouseClicked):
      #   for button in photo_capture_buttons:
      #     if button["target"].collidepoint((mousex, mousey)):
      #       if (button["value"] == BUTTON_PHOTO_CAPTURE):
      #         filename = toulouse.get_photos_filename()
      #         print("Taking Picture", filename)
      #         try:
      #           camera.capture(filename, use_video_port=False, format='jpeg', thumbnail=None)
      #           # Set image file ownership to pi user, mode to 644
      #           os.chmod(filename, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
      #         finally:
      #           # Convert to Curves File
      #           # python process.py image1.jpg output1 no
      #       if (button["value"] == BUTTON_CUSD_CLEAR):
      #         cusd_queue_id = None
    elif (toulouse.page == ui.state.Page.CURVES_SELECTION_SCREEN):
      if (not toulouse.loaded_new_state):
        print("----> Displaying Curves Selection Screen")
        # Create Sorted List of Files
        files = toulouse.curve_files()

        # Set Maximum Scroll Y Max
        scroll_y = 0 # reset scroll
        scroll_y_max = -(ui.curvesselection.BUTTON_YSIZE+ui.curvesselection.BUTTON_YGAP)*len(files)
        scroll_y_max += settings.WINDOWHEIGHT-settings.UI_MARGIN_TOP
        toulouse.loaded_screen(ui.state.Page.CURVES_SELECTION_SCREEN)

      DISPLAYSURF.fill(ui.colours.SCREEN_BG_COLOR)

      files_buttons = []
      for i in range(len(files)):
        files_buttons.append(ui.curvesselection.rounded_button(DISPLAYSURF, files[i], 
          settings.UI_MARGIN, settings.UI_MARGIN_TOP + scroll_y +(ui.curvesselection.BUTTON_YSIZE+ui.curvesselection.BUTTON_YGAP)*i))

      ui.utilities.Header(DISPLAYSURF, toulouse, "Programs", ui.colours.PHOSPHORIC_LIGHT_COLOR)

      # Button Logic
      if (mouseClicked):
        for button in files_buttons:
          if button["target"].collidepoint((mousex, mousey)):
            if (button["value"] == ui.curvesselection.BUTTON_FILE):
              print("      Starting Processing on Curves File:", button["action"])
              toulouse.load_program(button["action"])
              toulouse.load_screen(ui.state.Page.HOME_SCREEN)
    elif (toulouse.page == ui.state.Page.MESSAGES_LIST_SCREEN):
      if (not toulouse.loaded_new_state):
        print("----> Displaying Message List Screen")
        scroll_y = 0 # reset scroll
        toulouse.loaded_screen(ui.state.Page.MESSAGES_LIST_SCREEN)

      DISPLAYSURF.fill(ui.colours.SCREEN_BG_COLOR)

      # Draw Buttons Once
      messages_buttons = []

      if (len(toulouse.messages) > 0):
        # Set Maximum Scroll Y Max
        scroll_y_max = -(ui.messages.BUTTON_YSIZE+ui.messages.BUTTON_YGAP)*len(toulouse.messages)
        scroll_y_max += settings.WINDOWHEIGHT-settings.UI_MARGIN_TOP
        scroll_y_max = scroll_y_max if scroll_y_max < 0 else 0

        message_len = len(toulouse.messages)
        for i in range(message_len):
          toulouse.messages[i]["id"] = i
          messages_buttons.append(ui.messages.rounded_button(DISPLAYSURF, toulouse.messages[-(i+1)], 
            settings.UI_MARGIN, settings.UI_MARGIN_TOP + scroll_y + (ui.messages.BUTTON_YSIZE+ui.messages.BUTTON_YGAP)*(i)))

      ui.utilities.Header(DISPLAYSURF, toulouse, "Messages")
      if (mouseClicked):
        for button in messages_buttons:
          if button["target"].collidepoint((mousex, mousey)):
            if button["value"] == ui.messages.BUTTON_LIST:
              message_id = button["action"]
              toulouse.load_screen(ui.state.Page.MESSAGE_SCREEN)
    elif (toulouse.page == ui.state.Page.MESSAGE_SCREEN):
      if (not toulouse.loaded_new_state):
        print("----> Displaying Message Screen")
        DISPLAYSURF.fill(ui.colours.SCREEN_BG_COLOR)
        messages_buttons = ui.messages.message_display(DISPLAYSURF, toulouse, toulouse.messages[message_id])
        toulouse.loaded_screen(ui.state.Page.MESSAGE_SCREEN)

      # Button Logic
      if (mouseClicked):
        for button in messages_buttons:
          if button["target"].collidepoint((mousex, mousey)):
            if (button["value"] == ui.messages.BUTTON_ACKNOWLEDGE):
              toulouse.mark_read(message_id)
              toulouse.load_screen(ui.state.Page.MESSAGES_LIST_SCREEN)
            elif (button["value"] == ui.messages.BUTTON_CLEAR):
              toulouse.load_screen(ui.state.Page.MESSAGES_LIST_SCREEN)
    elif (toulouse.page == ui.state.Page.HOME_AXES_SCREEN):
      if (not toulouse.loaded_new_state):
        print("----> Displaying Home Axes Screen")
        homeaxes_buttons = ui.homeaxes.message_display(DISPLAYSURF, toulouse)
        toulouse.loaded_screen(ui.state.Page.HOME_AXES_SCREEN)

      # Button Logic
      if (mouseClicked):
        for button in homeaxes_buttons:
          if button["target"].collidepoint((mousex, mousey)):
            if (button["value"] == ui.homeaxes.BUTTON_ACKNOWLEDGE):
              toulouse.home_axes()
    else: # Display Home Screen
      if (toulouse.mode == ui.state.Mode.NO_MODE_CHOSEN):
        toulouse.load_screen(ui.state.Page.HOME_AXES_SCREEN)
      if (not toulouse.loaded_new_state):
        print("----> Displaying Home Screen")
        toulouse.loaded_screen(ui.state.Page.HOME_SCREEN)

      DISPLAYSURF.fill(ui.colours.SCREEN_BG_COLOR)

      # Draw Buttons Once
      ui.utilities.Header(DISPLAYSURF, toulouse, "")

      for i in range(len(ui.home.GLANCES)):
        ui.home.glance(DISPLAYSURF, toulouse, ui.home.GLANCES[i], settings.UI_MARGIN_TOP+(ui.home.GLANCE_YSIZE+ui.home.GLANCE_YGAP)*i)

    # Redraw the screen and wait a clock tick.
    pygame.display.update()
    FPSCLOCK.tick(ui.settings.FPS)

if __name__ == '__main__':
    main()