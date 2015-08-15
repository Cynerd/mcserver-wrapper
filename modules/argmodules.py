import re
import utils
from utils import conf

services = (
		utils.Service.argument,
		)

__add_modules__ = set()

def argument(args):
	global __add_modules__
	if not re.search('^--modules=', args[0]):
		return 0
	__add_modules__ = args[0][10:].split(',')
	return 1

def argument_short(l, args):
	global __add_modules__
	if l == 'm':
		if len(args) < 1:
			return 0
		__add_modules__ = args[0].split(',')
		return 1
	return 0

def argument_exec():
	for mod in __add_modules__:
		conf.modules.add(mod)
	
def argument_help():
	if conf.action == 'start' or conf.action == 'list-modules':
		print('   -m MODULE,...  --module=MODULE,...')
		print('       Load additional server modules. Multiple modules can be')
		print('       specified. Separate them using commas.')
