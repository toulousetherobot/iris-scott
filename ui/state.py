"""
Created on April 17, 2017
@author: aramael
"""
from enum import Enum
from datetime import datetime

class Mode(Enum):
	STOP_CATEGORY_ZERO = 0
	STOP_CATEGORY_ONE  = 1
	STOP_CATEGORY_TWO  = 2

	NO_MODE_CHOSEN   = 10
	NORMAL_MODE      = 11
	MANUAL_MODE      = 12
	MAINTENANCE_MODE = 13

class Page(Enum):
	SPLASH_SCREEN = 1
	PASSCODE_LOCK_SCREEN = 2
	HOME_SCREEN = 3
	MAIN_MENU_SCREEN = 4
	MANUAL_JOG_CARTESIAN_SCREEN = 5
	MANUAL_JOG_JOINT_SCREEN = 6
	PROGRAM_SELECTION_SCREEN = 7
	PHOTO_CAPTURE_SCREEN = 8
	CURVES_SELECTION_SCREEN = 9
	MESSAGES_LIST_SCREEN = 10
	MESSAGE_SCREEN = 11

class Toulouse(object):
	def __init__(self):

		self.status = Mode.NO_MODE_CHOSEN

		self.previous_OS_states = []

		# Set Up Splash Screen
		self.page = Page.SPLASH_SCREEN

	# Space to Load Up Any Other Programs Required
	def load(self):
		pass