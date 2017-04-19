"""
Created on April 17, 2017
@author: aramael
"""
import os
import subprocess

from enum import Enum
from datetime import datetime
from copy import deepcopy
from math import cos, sin

class Mode(Enum):
	STOP_CATEGORY_ZERO = 0
	STOP_CATEGORY_ONE  = 1
	STOP_CATEGORY_TWO  = 2

	NO_MODE_CHOSEN   = 10
	NORMAL_MODE      = 11
	MANUAL_MODE      = 12
	MAINTENANCE_MODE = 13

class Page(Enum):
	NO_SCREEN_CHOSEN = 0
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

class State(object):
	def __init__(self, mode, page, theta1, theta2, d3, program, frame):
		self.timestamp = datetime.now()
		self.mode = mode
		self.page = page
		self.theta1 = theta1
		self.theta2 = theta2
		self.d3 = d3
		self.program = program
		self.frame = frame

	def __str__(self):
		return "{time}: Mode <{mode}>, Page <{page}>, Program <{program}>, T1 <{theta1}>, T2 <{theta2}>, D3 <{d3}>".format(
			time=self.timestamp, mode=self.mode, page=self.page, program=self.program, theta1=self.theta1, theta2=self.theta2, d3=self.d3)

class Toulouse(object):
	SHOULDER_PAN_LINK_LENGTH = 8.75
	ELBOW_PAN_LINK_LENGTH = 8.75

	CURVES_FOLDER = "curves"
	CURVES_EXT = ".crv"
	CURVES_PREPROCESSED_EXT = ".pkt"

	def __init__(self):

		self.mode = Mode.NO_MODE_CHOSEN
		self.page = Page.NO_SCREEN_CHOSEN
		self.loaded_new_state = False
		self.program = None
		self.frame = None
		self.total_frames = None
		self.curves_path = None

		# Joint Angles
		self.theta1 = None
		self.theta2 = None
		self.d3     = None

		self.previous_OS_states = []

		# Set Up Authorisation
		self.locked = True
		self.passcode = [1, 9, 0, 1]
		self.passcode_failed_attempts_counter = 0

		# Set Up Splash Screen
		self.load_screen(Page.SPLASH_SCREEN)

	def new_state(self, mode=None, page=None, theta1=None, theta2=None, d3=None, program=None, frame=None):
		if (len(self.previous_OS_states) == 0):
			# No New States
			state = State(mode=self.mode, page=self.page, theta1=None, theta2=None, d3=None, program=None, frame=None)
		else:
			state = deepcopy(self.previous_OS_states[-1])

			# Update Selectively
			state.mode = mode if mode is not None else state.mode
			state.page = page if page is not None else state.page
			state.theta1 = theta1 if theta1 is not None else state.theta1
			state.theta2 = theta2 if theta2 is not None else state.theta2
			state.d3 = d3 if d3 is not None else state.d3
			state.program = program if program is not None else state.program
			state.frame = frame if frame is not None else state.frame

		# Change State of Toulouse if Defined
		if (mode is not None):
			self.mode = mode
		if (page is not None):
			self.page = page
		if (theta1 is not None):
			self.theta1 = theta1
		if (theta2 is not None):
			self.theta2 = theta2
		if (d3 is not None):
			self.d3 = d3
		if (program is not None):
			self.program = program
		if (frame is not None):
			self.frame = frame

		print(state)
		self.previous_OS_states.append(state)

	def load_screen(self, page):
		if (self.page != page):
			self.new_state(page=page)
			self.loaded_new_state = False
			return True
		return False

	def loaded_screen(self, page):
		if (self.page == page):
			self.loaded_new_state = True
		return self.loaded_new_state

	def login(self, passcode_attempt):
		if (len(passcode_attempt) >= len(self.passcode)):
			# Passcode Entered Successfully
			if (passcode_attempt == self.passcode):
				self.passcode_failed_attempts_counter = 0
				self.locked = False
				return self.load_screen(Page.HOME_SCREEN)
			else:
				self.passcode_failed_attempts_counter += 1
				return False
		return -1

	def lock(self):
		if (not self.locked):
			self.locked = True

	def restart(self):
		print("      ATTENTION, TOULOUSE POWER TO BE CYCLED IMMEDIATELY. PLEASE STAND CLEAR.")
		exit(0)

	def shutdown(self):
		print("      ATTENTION, TOULOUSE TO BE POWERED DOWN IMMEDIATELY. PLEASE STAND CLEAR.")
		exit(0)

	def load_program(self, program):
		if (self.program != program):
			# Check Program still exists
			if (os.path.exists(os.path.join(self.curves_path, program))):

				# Pre-Process `.crv` file
				program = os.path.join(Toulouse.CURVES_FOLDER, program)
				program_stat = os.stat(program)

				pkt_file = program.replace(Toulouse.CURVES_EXT, Toulouse.CURVES_PREPROCESSED_EXT)

				if (os.path.exists(pkt_file)):
					pkt_file_stat = os.stat(pkt_file)

					if (program_stat.st_mtime > pkt_file_stat.st_mtime):
						print ("      Program is Newer than Pre-Processed Packets")

						subprocess.run(["./crvpreprocessor", program, pkt_file])
				else:
						print ("      Pre-Processed Program to Packets")
						subprocess.run(["./crvpreprocessor", program, pkt_file])					

				pkt_file_stat = os.stat(pkt_file)
				if (pkt_file_stat.st_size%12 == 0):
					self.total_frames = int(pkt_file_stat.st_size/12)

				self.new_state(program=program, frame=0)
				return True
		return False

	def curve_files(self):
		# Create Sorted List of Files
		files = []
		for (dirpath, dirnames, filenames) in os.walk(self.curves_path):
			files.extend(filenames)
			break

		# `.crv` files only
		files = [file for file in files if file.endswith(Toulouse.CURVES_EXT)]
		sorted(files)

		return files

	# X
	@property
	def X(self):
		return Toulouse.SHOULDER_PAN_LINK_LENGTH*cos(self.theta1)+Toulouse.ELBOW_PAN_LINK_LENGTH*cos(self.theta1-self.theta2)

	# Y
	@property
	def Y(self):
		return Toulouse.SHOULDER_PAN_LINK_LENGTH*sin(self.theta1)+Toulouse.ELBOW_PAN_LINK_LENGTH*sin(self.theta1-self.theta2)

	# Z
	@property
	def Z(self):
		return self.d3

	# Space to Load Up Any Other Programs Required
	def load(self):
		# Check Curves Directory Exists & If Not Create One
		current_directory = os.getcwd()
		curves_path = os.path.join(current_directory, Toulouse.CURVES_FOLDER)
		if not os.path.exists(curves_path):
		  os.makedirs(curves_path, exist_ok=True)
		self.curves_path = curves_path