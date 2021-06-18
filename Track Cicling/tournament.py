from __future__ import annotations
from typing import Callable, List, Optional
from functools import total_ordering
from random import shuffle


@total_ordering
class Cyclist:
    def __init__(self, time_function: Callable[[], float]):
        self._time_function = time_function
        self._times: List[float] = []

    @property
    def time(self) -> float:
        time: float = self._time_function()
        self._times.append(time)
        return time

    @property
    def last_time(self) -> float:
        return self._times[-1]

    @property
    def times(self) -> List[float]:
        return self._times[:]

    def __lt__(self, other: Cyclist) -> bool:
        return self.time < other.time


class Tournament:
    def __init__(self, cyclists: List[Cyclist]):
        self._cyclists: List[Cyclist] = cyclists
        self._accepted: List[Cyclist] = []
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

    def _qualifying_round(self):
        results: List[Cyclist] = list(sorted(self._cyclists))
        self._accepted = results[:24]

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

    def _repechage3(self):
        repechage: List[Cyclist] = self._repechage3_list[:]
        shuffle(repechage)
        g1: List[Cyclist] = list(sorted(repechage[:3]))
        g2: List[Cyclist] = list(sorted(repechage[3:6]))
        self._round3_winners.append(g1[0])
        self._round3_winners.append(g2[0])

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

    def final(self):
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
