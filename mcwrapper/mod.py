# vim: expandtab ft=python ts=4 sw=4 sts=4:
import random

from . import alarm
from . import prints


class MoD:
    "Message of the day handler"
    def __init__(self, mcwrapper, file, period=900):
        self.mcwrapper = mcwrapper
        self.file = file
        alarm.set("mod-time", period, self.__handler__, repeat=True)

    def __handler__(self):
        lines = []
        try:
            with open(self.file, "r") as f:
                lines = f.readlines()
        except OSError as e:
            prints.warning("Loading of MoD file failed: " + str(e))
            return
        if len(lines) > 0:
            i = random.randint(0, len(lines) - 1)
            self.mcwrapper.write_to_terminal("/say " + lines[i].rstrip() +
                                             "\n")
