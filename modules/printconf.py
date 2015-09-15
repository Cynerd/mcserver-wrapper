import os
import sys
import re
import utils
from utils import conf

services = (
		utils.Service.argument,
		utils.Service.action,
		)

__conf_file__ = False

def argument(args):
	global __conf_file__
	if args[0] == '--file':
		__conf_file__ = True
		return 1

def argument_short(l, args):
	return 0

def argument_exec():
	conf.argument_conffile = __conf_file__

def argument_help():
	if conf.action == 'config':
		print('   --file')
		print('       Print only used configuration file.')
	
def action(args):
	if conf.action == None and args[0].lower() == 'config':
		conf.action = 'config'
		conf.action_module = sys.modules[__name__]
		return 1
	return 0

def action_exec():
	if conf.argument_conffile:
		try:
			print(conf.__file__)
		except AttributeError:
			print('Default configuration used. No file associated.')
	else:
		print('TODO')

def action_help():
	pass

def action_full_help():
	pass
