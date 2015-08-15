# This is python file with usable utilities for modules
# This can't be used as mcwrapper module. Although it's not a problem if loaded.
import os
import datetime
import re
import struct
import traceback
from enum import Enum

# Dummy variable to be used before it is set by mcwrapper
conf = type('defconf', (object,), {})

class Service(Enum):
	# Request service of conf function
	# This function is called right after argument parsing.
	# Configuration is loaded before almost anything is done.
	# Prototype: config(conf)
	#   Where conf is class containing configuration variables.
	config = 1
	# Request service of init function
	# This function is called right before Minecraft server is started.
	# Prototype: init()
	init = 2
	# Request service of clean function
	# This function is called before mcwrapper exits.
	# Prototype: clean()
	clean = 3
	# Request service of parse function
	# Prototype: parse(line)
	#   Where line is line from Minecraft server standard and error output.
	parse = 4
	# Signalize that exceptions shouldn't be ignored.
	# Otherwise exception is printed and module is removed.
	exceptionThrow = 101
	# Requests service of action and action_help function.
	# This flag can't be denied by serviceServer or by configuration.
	# Prototype: action(act, args)
	#   Where act is string specifying action and args are rest of command line
	#   arguments.
	# Prototype: action_help()
	action = 201
	# Requests service of argument function.
	# This flag can't be denied by serviceServer or by configuration.
	# Prototype: argument(arg, args)
	#   Where arg is parser argument and args are rest of command line arguments.
	argument = 202
	def toStr(service):
		if service == Service.config:
			return 'S-Config'
		elif service == Service.init:
			return 'S-Init'
		elif service == Service.clean:
			return 'S-Clean'
		elif service == Service.parse:
			return 'S-Parse'
		elif service == Service.exceptionThrow:
			return 'F-ExceptionThrow'
		elif service == Service.action:
			return 'P-Action'
		elif service == Service.argument:
			return 'P-Argument'

def __module_disable__(module):
	"""Disable specified module"""
	if verbose_level >= 0:
		print('Disabling module: ' + str(module))
	if Service.clean in module.services:
		try:
			module.clean()
		except Exception:
			traceback.print_exc()
	for name, value in vars(conf).items():
		if re.search('^__modules', name):
			try:
				value.remove(module)
			except KeyError:
				pass
	del module

def printArgumentsHelp():
	"""Prints help for all arguments from loaded modules"""
	print('   -h, --help')
	print('       Prints this help text.')
	print('   -v, --verbose')
	print('       Increase verbose level of output.')
	print('   -q, --quiet')
	print('       Decrease verbose level of output.')
	for mod in conf.__modules_argument__:
		mod.argument_help()

def serviceCall(servicename, func, argv=[], mode=0):
	"""Calls func in all/n-th modules with specified service.
	
	  servicename - String name of service
	  func - String name of functions to be called
	  argv - List of arguments passed to functions
	  mode - Mode of execution
			 0 - called for every module without result returning
	         1 - called for every module and return result
			 2 - called until True is returned from function called
	"""	
	def execmod(servicename, func, argv, mod):
		cmd = 'mod.' + func + '( '
		for i in range(0, len(argv)):
			cmd += 'argv[' + str(i) + '],'
		cmd = cmd[0:len(cmd)-1] + ')'
		try:
			return eval(cmd)
		except Exception as e:
			if Service.exceptionThrow in mod.services:
				raise e
			else:
				traceback.print_exc()
				__module_disable__(mod)
				return None
	if mode == 0:
		for mod in vars(conf)['__modules_' + servicename + '__'].copy():
			execmod(servicename, func, argv, mod)
		return 
	elif mode == 1:
		ret = dict()
		for mod in vars(conf)['__modules_' + servicename + '__'].copy():
			ret[mod] = execmod(servicename, func, argv, mod)
		return ret
	elif mode == 2:
		for mod in vars(conf)['__modules_' + servicename + '__'].copy():
			rtn = execmod(servicename, func, argv, mod)
			if rtn:
				return rtn, mod
		return None, None

def isServerRunning():
	"""Check if server is running. It checks if input_pipe exists.
	Returns:
	  True  - Running in any state or residue pipe exists.
	  False - Not running
	"""
	return os.path.exists(conf.inputPipe)

__default_config__ = {
		"modules": {'say', 'argmodules', 'list-modules', 'printconf'},
		"identifier": None,
		}
__default_server_config__ = {
		"modules": {'status', 'players'},
		"folder": '/dev/shm/mcwrapper-exampleserver',
		"logOutput": False,
		"logFile": datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S') + '.log',
		"command": [],
		}

def setServerConf(identifier):
	"""Sets server configuration."""
	conf.identifier = identifier
	try:
		conf.server[identifier]
		vars(conf).update(conf.server[identifier])
	except AttributeError:
		if conf.verbose_level >= 0:
			print('W: No configuration associated with identifier: "' + conf.identifier)
	configSet(__default_server_config__)
	# Set additional runtime configuration variables
	conf.inputPipe = conf.folder + '/input_pipe'

def configSet(confs):
	"""This is for setting default configurations. If configuration for module is
	not set in conf file, then it must be set while module initialization.

	confs - dictionary of configuration options and default values.
	"""
	for name, val in confs.items():
		try:
			dir(conf).index(name)
		except ValueError:
			exec('conf.' + name + '=val')

def varint_unpack(data):
	"Returns varint value from beginning of data and number of bytes used."
	i = 0
	nextbt = True
	newdata = 0
	while nextbt:
		bt = data[i]
		if not bt & (1 << 7):
			nextbt = False
		bt = bt & ~(1 << 7)
		newdata = newdata | (bt << (i * 7))
		print(newdata)
	return newdata, i

def varint_pack(integer):
	pass

#################################################################################
## dummy module
services = ()
