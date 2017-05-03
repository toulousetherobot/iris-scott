"""
Created on April 17, 2017
@author: aramael
"""
import os
import stat
import subprocess
import pika
import json
import socket

from enum import Enum
from datetime import datetime
from copy import deepcopy
from math import cos, sin, sqrt, atan2

def check_exists_or_make_directory(path):
    if not os.path.isdir(path):
        try:
            os.makedirs(path)

            # Set new directory ownership to pi user, mode to 755
            os.chown(path, uid, gid)
            os.chmod(path,
            stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
            stat.S_IRGRP | stat.S_IXGRP |
            stat.S_IROTH | stat.S_IXOTH)
        except OSError as e:
            # errno = 2 if can't create folder
            print(e.errno)
    return path

class Mode(Enum):
	STOP_CATEGORY_ZERO = 0
	STOP_CATEGORY_ONE  = 1
	STOP_CATEGORY_TWO  = 2

	STOP_MODES = [STOP_CATEGORY_ZERO, STOP_CATEGORY_ONE, STOP_CATEGORY_TWO]

	NO_MODE_CHOSEN   = 10
	NORMAL_MODE      = 11
	MANUAL_MODE      = 12
	MAINTENANCE_MODE = 13

	UNINITIALIZED_MODE = 20
	INITIALIZED_MODE = 21

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
	HOME_AXES_SCREEN = 12

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
	HANDEDNESS = 1
	SHOULDER_PAN_LINK_LENGTH = 8.75
	ELBOW_PAN_LINK_LENGTH = 8.75

	PHOTOS_FOLDER = "photos"
	CURVES_FOLDER = "curves"
	CURVES_EXT = ".crv"
	CURVES_PREPROCESSED_EXT = ".pkt"

	def __init__(self, running_on_pi):

		self.running_on_pi = running_on_pi
		self.mode = Mode.UNINITIALIZED_MODE
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

		# Set Up Messages
		self.message_unread_count = 0
		self.messages = []

		# IP Address
		self.inetaddr = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

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
				self.new_state(mode=Mode.NO_MODE_CHOSEN)
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
		if (self.running_on_pi):
			os.system("sudo shutdown -h now")
		exit(0)

	def process_caricature(self):
		filename = toulouse.get_photos_filename()
			print("Taking Picture", filename)
		try:
			camera.capture(filename, use_video_port=False, format='jpeg', thumbnail=None)
			# Set image file ownership to pi user, mode to 644
			os.chmod(filename, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
			self.load_screen(Page.HOME_SCREEN)
		finally:
			output_file = os.path.splitext(filename)[0]
			output_file = os.path.basename(filename)
			curves_file = output_file + ".crv"
			full_curves_file = os.path.join(self.curves_path, curves_file)
		# Convert to Curves File
			subprocess.run(["python", "/home/pi/image-processing/cv/process.py", filename, full_curves_file, "no"])
			self.load_program(curves_file)
			pkt_file = program.replace(Toulouse.CURVES_EXT, Toulouse.CURVES_PREPROCESSED_EXT)
			subprocess.Popen(["/home/pi/toulouseos/draw", pkt_file])

	def back(self):
		if (not self.locked and self.page != Page.HOME_SCREEN):
			prev_page = self.previous_OS_states[-2].page
			if (prev_page in [Page.NO_SCREEN_CHOSEN, Page.SPLASH_SCREEN, Page.PASSCODE_LOCK_SCREEN] or 
				self.page in [Page.MANUAL_JOG_CARTESIAN_SCREEN, Page.MANUAL_JOG_JOINT_SCREEN, Page.PROGRAM_SELECTION_SCREEN, Page.MESSAGES_LIST_SCREEN]):
				prev_page = Page.HOME_SCREEN
			return self.load_screen(prev_page)

	def home_axes(self):
		self.new_state(mode=Mode.MANUAL_MODE, theta1=0, theta2=0, d3=0)
		return self.load_screen(Page.HOME_SCREEN)

	def load_program(self, program):
		if (self.program != program):
			# Check Program still exists
			if (os.path.exists(os.path.join(self.curves_path, program))):

				# Pre-Process `.crv` file
				program_name = deepcopy(program)
				program = os.path.join(Toulouse.CURVES_FOLDER, program)
				program_stat = os.stat(program)

				pkt_file = program.replace(Toulouse.CURVES_EXT, Toulouse.CURVES_PREPROCESSED_EXT)

				if (os.path.exists(pkt_file)):
					pkt_file_stat = os.stat(pkt_file)

					if (program_stat.st_mtime > pkt_file_stat.st_mtime):
						self.new_message("info", "Old Packets", "Requesting an updated set of packets.")

						subprocess.run(["/home/pi/toulouseos/crvpreprocessor", program, pkt_file])
						self.new_message("success", "Pre-Processed Packets", program_name)
				else:
						subprocess.run(["/home/pi/toulouseos/crvpreprocessor", program, pkt_file])					
						self.new_message("success", "Pre-Processed Packets", program_name)

				pkt_file_stat = os.stat(pkt_file)
				if (pkt_file_stat.st_size%12 == 0):
					self.total_frames = int(pkt_file_stat.st_size/12)

				self.new_state(program=program, frame=0)
				self.new_message("success", "Loaded Program", program_name)
				return True
		return False

	def get_photos_filename(self):
		# Scan for next available image slot
		id = 0
		while True:
			filename = os.path.join(self.photos_path, "IMG_{:04d}.jpg".format(id))
			if not os.path.isfile(filename):
				return filename
			id += 1
			if id > 9999: id = 0

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

	def inverse_kinematics(self, x, y):
		r = (x**2+y**2-Toulouse.SHOULDER_PAN_LINK_LENGTH**2-Toulouse.ELBOW_PAN_LINK_LENGTH**2)/(2*Toulouse.SHOULDER_PAN_LINK_LENGTH*Toulouse.ELBOW_PAN_LINK_LENGTH)
		theta2 = atan2(Toulouse.HANDEDNESS*sqrt(1-r**2), r)
		theta1 = atan2(y, x)-atan2(Toulouse.ELBOW_PAN_LINK_LENGTH*sin(theta2), Toulouse.SHOULDER_PAN_LINK_LENGTH+Toulouse.ELBOW_PAN_LINK_LENGTH*cos(theta2))
		self.new_state(theta1=theta1, theta2=theta2)

	# THETA1
	@property
	def THETA1(self):
		return self.theta1

	@THETA1.setter
	def THETA1(self, value):
		self.new_state(theta1=value)

	# THETA2
	@property
	def THETA2(self):
		return self.theta2

	@THETA2.setter
	def THETA2(self, value):
		self.new_state(theta2=value)

	# D3
	@property
	def D3(self):
		return self.d3

	@D3.setter
	def D3(self, value):
		self.new_state(d3=value)

	# X
	@property
	def X(self):
		if self.theta1 is not None or self.theta2 is not None:
			return Toulouse.SHOULDER_PAN_LINK_LENGTH*cos(self.theta1)+Toulouse.ELBOW_PAN_LINK_LENGTH*cos(self.theta1+self.theta2)

	@X.setter
	def X(self, value):
		self.inverse_kinematics(value, self.Y)

	# Y
	@property
	def Y(self):
		if self.theta1 is not None or self.theta2 is not None:
			return Toulouse.SHOULDER_PAN_LINK_LENGTH*sin(self.theta1)+Toulouse.ELBOW_PAN_LINK_LENGTH*sin(self.theta1+self.theta2)

	@Y.setter
	def Y(self, value):
		self.inverse_kinematics(self.X, value)

	# Z
	@property
	def Z(self):
		if self.theta1 is not None or self.theta2 is not None:
			return self.d3

	@Z.setter
	def Z(self, value):
		self.new_state(d3=value)

	def new_message(self, type, title, footnote):
		if (type not in ["error", "warning", "success", "info"]):
			return False

		message = {
			"type": type,
			"title": title,
			"footnote": footnote,
			"timestamp": datetime.now(),
			"read": False
		}

		self.messages.append(message)
		self.message_unread_count += 1

	def mark_read(self, index):
		if (0 <= index < len(self.messages)):
			self.messages[index]["read"] = True
			self.message_unread_count -= 1
			return True
		return False

	def check_messages(self):
		method_frame, properties, body = self.channel.basic_get('messages')
		if method_frame is None:
			return

		message = json.loads(body)
		self.new_message(type=message.get("type"), title=message.get("title"), footnote=message.get("footnote"))

		# Acknowledge the message
		self.channel.basic_ack(method_frame.delivery_tag)

	# Space to Load Up Any Other Programs Required
	def load(self):
		# Check Curves Directory Exists & If Not Create One
		current_directory = os.getcwd()
		self.curves_path = check_exists_or_make_directory(os.path.join(current_directory, Toulouse.CURVES_FOLDER))
		self.photos_path = check_exists_or_make_directory(os.path.join(current_directory, Toulouse.PHOTOS_FOLDER))

		# Set Up Messages
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='messages')

		self.new_state(mode=Mode.INITIALIZED_MODE)