import sys
import re
import utils
from utils import conf
import importlib.machinery as imp

services = (
		utils.Service.action,
		)

def action(args):
	if conf.action == None:
		if args[0].lower() != 'list-modules':
			return False
		conf.action = 'list-modules'
		conf.action_module = sys.modules[__name__]
		return 1
	elif conf.identifier == None:
		conf.identifier = args[0]
		return 1
	return 0

def action_exec():
	if conf.verbose_level >= 1:
		for mod in conf.modules:
			try:
				module = imp.SourceFileLoader(mod,
						conf.modulesFolder + '/' + mod + '.py').load_module()
				print(module)
				for service in module.services:
					print('  ' + utils.Service.toStr(service))
			except FileNotFoundError:
				sys.exit('Unknown module: ' + mod)
	else:
		# TODO add check if module exists
		for mod in conf.modules:
			print(mod)

def action_help():
	print('   list-modules')
	print('       List all modules that will be used.')

def action_full_help():
	print('mcwrapper [arguments...] list-modules [IDENTIFIER]')
	print('  List all modules that will be used.')
	print('')
	print(' arguments')
	utils.printArgumentsHelp()
	print(' IDENTIFIER')
	print('   Identifier of Minecraft server instance.')
	print('   If specified, server modules are printed.')
