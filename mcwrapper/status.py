# vim: expandtab ft=python ts=4 sw=4 sts=4:
import os

from . import prints

__STATUSSTRINGS__ = {
    0: "Not running",
    1: "Starting",
    2: "Running",
    3: "Stopping",
    }
__STATUSFILE__ = 'status'


class MCStatus:
    "Tracks server status"
    def __init__(self, wrapper, file_export=False):
        self.wrapper = wrapper
        self.status = 0
        wrapper.hook_start(self.__server_start__)
        wrapper.hook_stop(self.__server_stop__)
        wrapper.hook_line(': Done', self.__server_started__)
        wrapper.hook_line(': Stopping the server', self.__server_stopping__)
        self.file_export = file_export
        if file_export:
            with open(__STATUSFILE__, 'w') as file:
                file.write(__STATUSSTRINGS__[0] + '\n')

    def clean(self):
        try:
            os.remove(__STATUSFILE__)
        except FileNotFoundError:
            pass

    def __server_start__(self):
        self.status = 1
        if self.file_export:
            with open(__STATUSFILE__, 'w') as file:
                file.write(__STATUSSTRINGS__[1] + '\n')

    def __server_stop__(self):
        if self.file_export:
            with open(__STATUSFILE__, 'w') as file:
                file.write(__STATUSSTRINGS__[0] + '\n')

    def __server_started__(self, line):
        prints.info("Server start.")
        self.status = 2
        if self.file_export:
            with open(__STATUSFILE__, 'w') as file:
                file.write(__STATUSSTRINGS__[2] + '\n')

    def __server_stopping__(self, line):
        prints.info("Server stop.")
        self.status = 3
        if self.file_export:
            with open(__STATUSFILE__, 'w') as file:
                file.write(__STATUSSTRINGS__[3] + '\n')
