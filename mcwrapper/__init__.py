# vim: expandtab ft=python ts=4 sw=4 sts=4:
import signal
import atexit
import argparse

from . import prints
from . import alarm
from .wrapper import MCWrapper
from .status import MCStatus
from .players import MCPlayers
from .mod import MoD

mcserver_wrapper = None
mcserver_status = None
mcserver_players = None
mcserver_mod = None


def __wrapper_atexit__():
    "This is called when wrapper is exiting"
    toclean = (
            mcserver_wrapper,
            mcserver_status,
            mcserver_players,
            mcserver_mod
            )
    for c in toclean:
        if c is not None:
            c.clean()


def __wrapper_toexit__():
    "This function is called when system signalizes that mcwrapper should exit"
    if mcserver_wrapper is not None:
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
    parser.add_argument('--mod-file', '-m', type=str,
                        help="""Prints periodically random line from
                        given file as message of the day.""")
    parser.add_argument('--mod-time', type=int,
                        help="""Period used for message of the day in
                        seconds. In default 900 (15 minutes).""")
    parser.add_argument('command', nargs=argparse.REMAINDER,
                        help="""Command to be executed to start Minecraft
                        server.""")
    args = parser.parse_args()

    prints.verbose_level = args.verbose - args.quiet
    command = args.command
    sfile = args.status_file
    pfile = args.players_file
    mod_file = args.mod_file
    mod_time = args.mod_time

    if not command:
        parser.print_help()
        return
    # Just small hack to not open minecraft server gui
    if 'nogui' not in command:
        command.append('nogui')

    alarm.init()

    atexit.register(__wrapper_atexit__)
    global mcserver_wrapper, mcserver_status, mcserver_players
    mcserver_wrapper = MCWrapper(command)
    signal.signal(signal.SIGTERM, __signal_term__)
    signal.signal(signal.SIGINT, __signal_term__)
    mcserver_status = MCStatus(mcserver_wrapper, sfile)
    mcserver_players = MCPlayers(mcserver_wrapper, pfile)

    mcserver_wrapper.start()
    if mod_file is not None:
        global mcserver_mod
        mcserver_mod = MoD(mcserver_wrapper, mod_file, mod_time or 900)
    mcserver_wrapper.process.wait()

if __name__ == '__main__':
    main()
