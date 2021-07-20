from random import random
import re
from typing import Callable, List
import math


class Athlete:
    def __init__(self, name: str, _fencing_prob: Callable[[], float], swiming: Callable[[], float], riding: Callable[[], float], laser_run: Callable[[], float]):
        self._name = name
        self._f_fencing_prob = _fencing_prob
        self._fencing_prob = None
        self.fencing_points = 0
        self.fencing_victories = 0
        self._swiming_time = None
        self._f_swiming = swiming
        self.swiming_points = 0
        self._f_reding = riding
        self._reding_points = None
        self._f_laser_run = laser_run
        self._laser_run_time = None
        self._handicap_time = 0

    def reset(self):
        self._fencing_prob = None
        self.fencing_points = 0
        self.fencing_victories = 0
        self._swiming_time = None
        self.swiming_points = 0
        self._reding_points = None
        self._laser_run_time = None
        self._handicap_time = 0

    @property
    def name(self):
        return self._name

    @property
    def fencing(self) -> bool:
        if self._fencing_prob is None:
            self._fencing_prob = self._f_fencing_prob()
        return random() < self._fencing_prob

    @property
    def swiming(self) -> float:
        if self._swiming_time is None:
            self._swiming_time = self._f_swiming()
        return self._swiming_time

    @property
    def riding(self) -> int:
        if self._reding_points is None:
            self._reding_points = int(self._f_reding())
        return self._reding_points

    @property
    def laserRun(self) -> float:
        if self._laser_run_time is None:
            self._laser_run_time = self._f_laser_run()
        return self._laser_run_time

    @property
    def points(self) -> int:
        return self.fencing_points + self.riding + self.swiming_points

    @property
    def handicapTime(self) -> float:
        return self._handicap_time

    @property
    def time(self) -> float:
        return self.laserRun + self.handicapTime


class Simulator:

    def __init__(self, athletes: List[Athlete]):
        self._athletes = athletes
        self.winners = []

    def fencing(self):
        for i in range(len(self._athletes) - 1):
            for j in range(i + 1, len(self._athletes)):
                a1: bool = self._athletes[i].fencing
                a2: bool = self._athletes[j].fencing
                result: bool = a1 ^ a2
                if not result:
                    if a1:
                        self._athletes[i].fencing_victories += 1
                    else:
                        self._athletes[j].fencing_victories += 1

        asault_point = 0
        if 22 <= len(self._athletes) <= 23:
            asault_point = 40
        elif 24 <= len(self._athletes) <= 26:
            asault_point = 36
        elif 27 <= len(self._athletes) <= 29:
            asault_point = 32
        elif 30 <= len(self._athletes) <= 33:
            asault_point = 28
        elif 34 <= len(self._athletes) <= 39:
            asault_point = 24

        seventy_percent = int(math.ceil((len(self._athletes) - 1) * 7 / 10))

        for athlete in self._athletes:
            points = 1000 + (athlete.fencing_victories -
                             seventy_percent) * asault_point
            athlete.fencing_points = points

    def swiming(self):
        time = 2 * 60 + 30
        for athlete in self._athletes:
            athlete.swiming_points = 1000 + (athlete.swiming - time) * 12

    def riding(self):
        for athlete in self._athletes:
            athlete.riding

    def laserRun(self):
        sorted_athletes = list(
            reversed(sorted(self._athletes, key=lambda a1: a1.points)))
        max_points = sorted_athletes[0].points

        for athlete in sorted_athletes:
            athlete._handicap_time = (max_points - athlete.points) / 4

        self.winners = sorted(self._athletes, key=lambda x: x.time)

    def run(self):
        self.fencing()
        self.swiming()
        self.riding()
        self.laserRun()

    def reset(self):
        self.winners = []
        for athlete in self._athletes:
            athlete.reset()
