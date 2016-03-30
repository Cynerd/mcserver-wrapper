# vim: expandtab ft=python ts=4 sw=4 sts=4:
import sys
import time

verbose_level = 0


def __print_message__(message, file=sys.stdout, notime=False):
    if notime:
        print(message, file=file)
    else:
        print('[' + time.strftime('%H:%M:%S') + '] ' + message, file=file)


def info(message, minverbose=0, notime=False):
    "Prints message to stdout if minverbose >= verbose_level"
    if verbose_level >= minverbose:
        __print_message__(message, notime=notime)


def warning(message, minverbose=-1, notime=False):
    "Prints message to stderr if minverbose >= verbose_level"
    if verbose_level >= minverbose:
        __print_message__(message, file=sys.stderr, notime=notime)


def error(message, minverbose=-2, errcode=-1, notime=False):
    "Prints message to stderr if minverbose >= verbose_level"
    if verbose_level >= minverbose:
        __print_message__(message, file=sys.stderr, notime=notime)
    sys.exit(errcode)

