# vim: expandtab ft=python ts=4 sw=4 sts=4:
import signal
import time

# Dict with alarms. Alarm is dictionary with initial time, alarm time and
# handler
__alarms__ = dict()
__alarm_wait__ = None


def __handler__(signum, frame):
    if __alarm_wait__["arg"] is not None:
        __alarm_wait__["handler"](__alarm_wait__["arg"])
    else:
        __alarm_wait__["handler"]()
    if not __alarm_wait__["repeat"]:
        __alarms__.pop(__alarm_wait__["name"])
    else:
        __alarm_wait__["time"] = __alarm_wait__["time"] + \
            __alarm_wait__["timeout"]
    __update__()


def __update__():
    lowest = None
    lowest_time = None
    now = time.time()
    for name, al in __alarms__.items():
        t = al["time"] + al["timeout"] - now
        if lowest_time is None or lowest_time > t:
            lowest_time = t
            lowest = al
    global __alarm_wait__
    if lowest is not None:
        if lowest_time < 1:
            # Less then second is missed alarm. Fire handler.
            __alarm_wait__ = lowest
            __handler__(None, None)
            return
        __alarm_wait__ = lowest
        signal.alarm(int(lowest_time))
    elif __alarm_wait__ is not None:
        signal.alarm(0)  # close any alarm
        __alarm_wait__ = None


def init():
    signal.signal(signal.SIGALRM, __handler__)  # prepare alarm


def set(name, t, handler, repeat=False, arg=None):
    al = dict()
    al["time"] = time.time()
    al["handler"] = handler
    al["timeout"] = t
    al["repeat"] = repeat
    al["arg"] = arg
    al["name"] = name
    __alarms__[name] = al
    __update__()


def unset(name):
    if name in __update__:
        __alarms__.pop(name)
        __update__()
