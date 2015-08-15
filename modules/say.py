import sys
import re
import utils
from utils import conf

services = (
		utils.Service.action,
		)

def action(args):
	if conf.action == None:
		if args[0].lower() != 'say':
			return False
		conf.action = 'say'
		conf.action_module = sys.modules[__name__]
		conf.sayMessage = []
		for arg in args[1:]:
			if conf.identifier == None:
				conf.identifier = arg
			else:
				conf.sayMessage.append(arg)
		return len(args)
	else:
		return 0

def action_exec():
	if not conf.sayMessage or not conf.identifier:
		action_full_help()
		return
	if not utils.isServerRunning():
		sys.exit("Server is not running or wrong identifier.")
	with open(sconf.inputPipe, 'w') as f:
		f.write("/say " + ' '.join(map(str, sconf.saymessage)) + '\n')
		f.flush()

def action_help():
	print('   say')
	print('       Sends message to Minecraft server chat.')

def action_full_help():
	print('mcwrapper [arguments...] say IDENTIFIER {message...}')
	print('  Sends message to Minecraft server chat.')
	print('')
	print(' arguments')
	utils.printArgumentsHelp()
	print(' IDENTIFIER')
	print('   Identifier of running server instance.')
	print(' message')
	print('   Message to be send to Minecraft server chat.')
