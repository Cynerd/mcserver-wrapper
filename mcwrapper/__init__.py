# vim: expandtab ft=python ts=4 sw=4 sts=4:
import os
import sys
import subprocess
import signal
import time
import atexit
import argparse
from threading import Thread

from . import prints
from . import wrapper
from .wrapper import MCWrapper

mcserver_wrapper = None


def __wrapper_atexit__():
    "This is called when wrapper is exiting"
    mcserver_wrapper.clean()


def __wrapper_toexit__():
    "This function is called when system signalizes that mcwrapper should exit"
    mcserver_wrapper.stop()


def __signal_term__(_signo, _stack_frame):
    __wrapper_toexit__()


__HELP_DESC__ = """
    This script is executing Minecraft server and reads its output. From output
    is extracted server status and list of online players. And standard input
    can be accessed by fifo file.
    """


def main():
    "Main function"
    global verbose_level
    parser = argparse.ArgumentParser(description=__HELP_DESC__)
    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help="Increase verbose level of output")
    parser.add_argument('--quiet', '-q', action='count', default=0,
                        help="Decrease verbose level of output")
    parser.add_argument('--status-file', '-s', action='store_true',
                        help="Outputs server status to file \"status\"")
    parser.add_argument('--players-file', '-p', action='store_true',
                        help="""Outputs list of online players to file
                        \"players\" """)
    parser.add_argument('command', nargs=argparse.REMAINDER,
                        help="""Command to be executed to start Minecraft
                        server.""")
    args = parser.parse_args()

    prints.verbose_level = args.verbose - args.quiet
    command = args.command
    sfile = args.status_file
    pfile = args.players_file

    if not command:
        parser.print_help()
        return
    if 'nogui' not in command:
        command.append('nogui')

    global mcserver_wrapper
    mcserver_wrapper = MCWrapper(command, pfile, sfile)
    signal.signal(signal.SIGTERM, __signal_term__)
    signal.signal(signal.SIGINT, __signal_term__)
    atexit.register(__wrapper_atexit__)

    mcserver_wrapper.execstart()

if __name__ == '__main__':
    main()
