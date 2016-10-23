# vim: expandtab ft=python ts=4 sw=4 sts=4:
import random

from . import alarm


class MoD:
    "Message of the day handler"
    def __init__(self, mcwrapper, file, period=900):
        self.mcwrapper = mcwrapper
        self.file = file
        self.load_mods()
        alarm.set("mod-time", period, self.__handler__, repeat=True)

    def load_mods(self):
        "Loads messages from self.file"
        with open(self.file, "r") as f:
            self.lines = f.readlines()

    def __handler__(self):
        if len(self.lines) > 0:
            i = random.randint(0, len(self.lines) - 1)
            self.mcwrapper.write_to_terminal("/say " + self.lines[i].rstrip()
                                             + "\n")
