# vim: expandtab ft=python ts=4 sw=4 sts=4:
import os

from . import prints

__PLAYERSFILE__ = 'players'


class MCPlayers:
    "Tracks online players"
    def __init__(self, wrapper, file_export=False):
        self.players = set()
        self.wrapper = wrapper
        wrapper.hook_start(self.__reset__)
        wrapper.hook_stop(self.__reset__)
        wrapper.hook_line('logged in with entity id', self.__user_join__)
        wrapper.hook_line('left the game', self.__user_leave__)
        self.file_export = file_export
        self.__reset__()

    def clean(self):
        try:
            os.remove(__PLAYERSFILE__)
        except FileNotFoundError:
            pass

    def __reset__(self):
        if self.file_export:
            open(__PLAYERSFILE__, 'w')  # Just create empty file

    def __user_join__(self, line):
        username = line[len('[00:00:00] [Server thread/INFO]: '):]
        username = username[:username.index('[')]
        prints.info("User '" + username + "' joined server.")
        self.players.add(username)
        if self.file_export:
            with open(__PLAYERSFILE__, 'a') as file:
                file.write(username + '\n')

    def __user_leave__(self, line):
        username = line[len('[00:00:00] [Server thread/INFO]: '):]
        username = username[:username.index(' ')]
        prints.info("User '" + username + "' left server.")
        self.players.remove(username)
        if self.file_export:
            with open(__PLAYERSFILE__, 'w') as file:
                file.write('\n'.join(self.players))
                if self.players:
                    file.write('\n')
