import os
import sys
import re
import utils
from utils import conf

services = (
		utils.Service.config,
		utils.Service.init,
		utils.Service.clean,
		utils.Service.parse,
		)

__STATUSSTRINGS__ = {
		0: "Not running",
		1: "Starting",
		2: "Running",
		3: "Stopping",
		}

def config(conf):
	conf.statusFile = conf.folder + '/status'

def init():
	with open(conf.statusFile, 'w') as f:
		f.write(__STATUSSTRINGS__[1])

def clean():
	os.remove(conf.statusFile)

def parse(line):
	if ': Done' in line:
		__server_start__()
	elif ': Stopping the server' in line:
		__server_stop__()
	else:
		return False
	return True

def __server_start__():
	print("Server start.")
	with open(conf.statusFile, 'w') as f:
		f.write(__STATUSSTRINGS__[2] + '\n')
	pass

def __server_stop__():
	print("Server stop.")
	with open(conf.statusFile, 'w') as f:
		f.write(__STATUSSTRINGS__[3] + '\n')
	pass

#### For other modules ####
def get_status(conf):
	"""Returns server status as number.
	Requires conf (server configuration) set with identifier using utils.confset().
	Returns:
	  0 - Not running
	  1 - Starting
	  2 - Running
	  3 - Stopping
	 -1 - Unknown status
	"""
	conf.statusFile = conf.folder + '/status'
	if not os.path.exists(conf.statusFile):
		return 0
	with open(conf.statusFile, 'r') as f:
		status = f.readline().rstrip()
		for i in range(len(__STATUSSTRINGS__)):
			if __STATUSSTRINGS__[i] == status:
				return i
		return -1
