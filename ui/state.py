"""
Created on April 17, 2017
@author: aramael
"""
from enum import Enum

class Mode(Enum):
	STOP_CATEGORY_ZERO = 0
	STOP_CATEGORY_ONE  = 1
	STOP_CATEGORY_TWO  = 2

	NORMAL_MODE      = 10
	MANUAL_MODE      = 11
	MAINTENANCE_MODE = 12

class State(object):
	pass
	# Timestamp
	# Mode
	# Theta 1
	# Theta 2
	# D3
	# Program
	# Screen

class Toulouse(object):
    def __init__(self):
    	self.status = Mode.NORMAL_MODE