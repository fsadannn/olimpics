from __future__ import annotations
from typing import Callable, List
from functools import total_ordering
from random import shuffle
import functools


@total_ordering
class Cyclist:
    def __init__(self, qualify_time_function: Callable[[], float], time_function: Callable[[], float], name: str, nation: str):
        self._name = name
        self._nation = nation
        self._time_function = time_function
        self._qualify_time_function = qualify_time_function
        self._times: List[float] = []
        self._is_in_qualification: bool = True
        self._qualification_time: float = None
        self._round_time: float = None

    def use_round(self):
        self._is_in_qualification = False

    def nex_time(self):
        self._round_time = self._time_function()
        self._times.append(self._round_time)

    def reset(self):
        self._is_in_qualification = True
        self._qualification_time = None
        self._round_time = None
        self._times: List[float] = []

    @property
    def name(self):
        return self._name

    @property
    def nation(self):
        return self._nation

    @property
    def time(self) -> float:
        if self._is_in_qualification:
            if self._qualification_time is not None:
                return self._qualification_time

            self._qualification_time = self._qualify_time_function()
            return self._qualification_time

        if self._round_time is None:
            self.nex_time()

        return self._round_time

    @property
    def last_time(self) -> float:
        return self._times[-1]

    @property
    def times(self) -> List[float]:
        return self._times[:]

    def __lt__(self, other: Cyclist) -> bool:
        return self.time < other.time


def generate_times(func):
    @functools.wraps(func)
    def wrapper_func(*args, **kwargs):
        tournament = args[0]
        for i in tournament._cyclists:
            i.nex_time()
        return func(*args, **kwargs)
    return wrapper_func


class Tournament:
    def __init__(self, cyclists: List[Cyclist]):
        self._cyclists: List[Cyclist] = cyclists
        self._accepted: List[Cyclist] = []
        self._qualification_results = []
        self._round1_winners: List[Cyclist] = []
        self._repechage1_list: List[Cyclist] = []
        self._round2_winners: List[Cyclist] = []
        self._repechage2_list: List[Cyclist] = []
        self._round3_winners: List[Cyclist] = []  # 1/8
        self._repechage3_list: List[Cyclist] = []
        self._quarterfinals_win: List[Cyclist] = []  # 1/4
        self._classification58: List[Cyclist] = []
        self._semifinal_win: List[Cyclist] = []
        self._bronze_list: List[Cyclist] = []
        self._final: List[Cyclist] = []
        self._bronze: List[Cyclist] = []
        self._win58: List[Cyclist] = []
        self._winners = None

    def reset(self):
        self._accepted: List[Cyclist] = []
        self._qualification_results = []
        self._round1_winners: List[Cyclist] = []
        self._repechage1_list: List[Cyclist] = []
        self._round2_winners: List[Cyclist] = []
        self._repechage2_list: List[Cyclist] = []
        self._round3_winners: List[Cyclist] = []  # 1/8
        self._repechage3_list: List[Cyclist] = []
        self._quarterfinals_win: List[Cyclist] = []  # 1/4
        self._classification58: List[Cyclist] = []
        self._semifinal_win: List[Cyclist] = []
        self._bronze_list: List[Cyclist] = []
        self._final: List[Cyclist] = []
        self._bronze: List[Cyclist] = []
        self._win58: List[Cyclist] = []
        self._winners = None
        for i in self._cyclists:
            i.reset()

    def run(self):
        self._qualifying_round()
        self._round1()
        self._repechage1()
        self._round2()
        self._repechage2()
        self._round3()
        self._repechage3()
        self._quarterfinals()
        self._semifinals()
        self._finals()

    @property
    def winners(self) -> List[Cyclist]:
        if self._winners is None:
            cyclists: List[Cyclist] = self._final + self._bronze + self._win58
            names = set()
            names.update(map(lambda x: x.name, cyclists))

            more_cyclists: List[Cyclist] = list(
                filter(lambda x: x.name not in names, self._repechage3_list))
            cyclists += more_cyclists
            names.update(map(lambda x: x.name, more_cyclists))

            more_cyclists: List[Cyclist] = list(
                filter(lambda x: x.name not in names, self._repechage2_list))
            cyclists += more_cyclists
            names.update(map(lambda x: x.name, more_cyclists))

            more_cyclists: List[Cyclist] = list(
                filter(lambda x: x.name not in names, self._repechage1_list))
            cyclists += more_cyclists
            names.update(map(lambda x: x.name, more_cyclists))

            more_cyclists: List[Cyclist] = list(
                filter(lambda x: x.name not in names, self._qualification_results))
            cyclists += more_cyclists
            names.update(map(lambda x: x.name, more_cyclists))

            self._winners = cyclists

        return self._winners

    def _qualifying_round(self):
        results: List[Cyclist] = list(sorted(self._cyclists))
        self._qualification_results = results
        self._accepted = results[:24]

        for i in self._cyclists:
            i.use_round()

    @generate_times
    def _round1(self):
        winners: List[Cyclist] = []
        louse: List[Cyclist] = []
        for i in range(len(self._accepted) // 2):
            cyclist1: Cyclist = self._accepted[i]
            cyclist2: Cyclist = self._accepted[-i - 1]
            if cyclist1 < cyclist2:
                winners.append(cyclist1)
                louse.append(cyclist2)
            else:
                winners.append(cyclist2)
                louse.append(cyclist1)

        self._round1_winners = winners
        self._repechage1_list = louse

    @generate_times
    def _repechage1(self):
        repechage1: List[Cyclist] = self._repechage1_list[:]
        shuffle(repechage1)
        g1: List[Cyclist] = list(sorted(repechage1[:3]))
        g2: List[Cyclist] = list(sorted(repechage1[3:6]))
        g3: List[Cyclist] = list(sorted(repechage1[6:9]))
        g4: List[Cyclist] = list(sorted(repechage1[9:12]))
        self._round1_winners.append(g1[0])
        self._round1_winners.append(g2[0])
        self._round1_winners.append(g3[0])
        self._round1_winners.append(g4[0])

    @generate_times
    def _round2(self):
        winners: List[Cyclist] = []
        louse: List[Cyclist] = []
        cyclists: List[Cyclist] = self._round1_winners
        shuffle(cyclists)
        for i in range(0, len(cyclists), 2):
            cyclist1: Cyclist = cyclists[i]
            cyclist2: Cyclist = cyclists[i + 1]
            if cyclist1 < cyclist2:
                winners.append(cyclist1)
                louse.append(cyclist2)
            else:
                winners.append(cyclist2)
                louse.append(cyclist1)

        self._round2_winners = winners
        self._repechage2_list = louse

    @generate_times
    def _repechage2(self):
        repechage: List[Cyclist] = self._repechage2_list[:]
        shuffle(repechage)
        g1: List[Cyclist] = list(sorted(repechage[:2]))
        g2: List[Cyclist] = list(sorted(repechage[2:4]))
        g3: List[Cyclist] = list(sorted(repechage[4:6]))
        g4: List[Cyclist] = list(sorted(repechage[6:8]))
        self._round2_winners.append(g1[0])
        self._round2_winners.append(g2[0])
        self._round2_winners.append(g3[0])
        self._round2_winners.append(g4[0])

    @generate_times
    def _round3(self):
        winners: List[Cyclist] = []
        louse: List[Cyclist] = []
        cyclists: List[Cyclist] = self._round2_winners
        shuffle(cyclists)
        for i in range(0, len(cyclists), 2):
            cyclist1: Cyclist = cyclists[i]
            cyclist2: Cyclist = cyclists[i + 1]
            if cyclist1 < cyclist2:
                winners.append(cyclist1)
                louse.append(cyclist2)
            else:
                winners.append(cyclist2)
                louse.append(cyclist1)

        self._round3_winners = winners
        self._repechage3_list = louse

    @generate_times
    def _repechage3(self):
        repechage: List[Cyclist] = self._repechage3_list[:]
        shuffle(repechage)
        g1: List[Cyclist] = list(sorted(repechage[:3]))
        g2: List[Cyclist] = list(sorted(repechage[3:6]))
        self._round3_winners.append(g1[0])
        self._round3_winners.append(g2[0])

    @generate_times
    def _quarterfinals(self):
        winners: List[Cyclist] = []
        louse: List[Cyclist] = []
        cyclists: List[Cyclist] = self._round3_winners
        shuffle(cyclists)
        for i in range(0, len(cyclists), 2):
            cyclist1: Cyclist = cyclists[i]
            cyclist2: Cyclist = cyclists[i + 1]
            cyclist1win: int = sum([cyclist1 < cyclist2,
                                    cyclist1 < cyclist2, cyclist1 < cyclist2])
            if cyclist1win > 1:
                winners.append(cyclist1)
                louse.append(cyclist2)
            else:
                winners.append(cyclist2)
                louse.append(cyclist1)

        self._quarterfinals_win = winners
        self._classification58 = louse

    @generate_times
    def _semifinals(self):
        winners: List[Cyclist] = []
        louse: List[Cyclist] = []
        cyclists: List[Cyclist] = self._quarterfinals_win
        shuffle(cyclists)
        for i in range(0, len(cyclists), 2):
            cyclist1: Cyclist = cyclists[i]
            cyclist2: Cyclist = cyclists[i + 1]
            cyclist1win: int = sum([cyclist1 < cyclist2,
                                    cyclist1 < cyclist2, cyclist1 < cyclist2])
            if cyclist1win > 1:
                winners.append(cyclist1)
                louse.append(cyclist2)
            else:
                winners.append(cyclist2)
                louse.append(cyclist1)

        self._semifinal_win = winners
        self._bronze_list = louse

    @generate_times
    def _finals(self):
        self._final = list(sorted(self._semifinal_win))
        cyclist1: Cyclist = self._bronze_list[0]
        cyclist2: Cyclist = self._bronze_list[1]
        cyclist1win: int = sum([cyclist1 < cyclist2,
                                cyclist1 < cyclist2, cyclist1 < cyclist2])
        if cyclist1win > 1:
            self._bronze.append(cyclist1)
            self._bronze.append(cyclist2)
        else:
            self._bronze.append(cyclist2)
            self._bronze.append(cyclist1)

        self._win58 = list(sorted(self._classification58))
