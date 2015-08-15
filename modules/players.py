import os
import sys
import re
import utils
from utils import conf

services = (
		utils.Service.config,
		utils.Service.init,
		utils.Service.clean,
		utils.Service.parse
		)

players = set()

def config(conf):
	conf.playersFile = conf.folder + '/players'

def init():
	with open(conf.playersFile, 'w') as f:
		pass

def clean():
	os.remove(conf.playersFile)

def parse(line):
	if 'logged in with entity id' in line:
		name = line[len('[00:00:00] [Server thread/INFO]: '):]
		name = name[:name.index('[')]
		__user_join__(name)
	elif 'left the game' in line:
		name = line[len('[00:00:00] [Server thread/INFO]: '):]
		name = name[:name.index(' ')]
		__user_leave__(name)
	else:
		return False
	return True


def __user_join__(username):
	print("User '" + username + "' joined server.")
	with open(conf.playersFile, 'a') as f:
		players.add(username)
		f.write(username + '\n')

def __user_leave__(username):
	print("User '" + username + "' left server.")
	players.remove(username)
	with open(conf.playersFile, 'w') as f:
		f.writelines(players)
		if players:
			f.write('\n')
