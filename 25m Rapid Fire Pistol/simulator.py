from __future__ import annotations
from typing import Callable, List
from functools import total_ordering, partial
import numpy as np


def get_sample(func):
    return func()[0]


@total_ordering
class Shooter:
    def __init__(self, qualify_points_function: Callable[[], float], final_prob_function: Callable[[], float], name: str, nation: str):
        self._name = name
        self._nation = nation
        self.final_prob_function = final_prob_function
        self._qualify_points_function = qualify_points_function
        self._q: float = None
        self._f: float = None
        self._finalist: bool = False
        self._final_function: Callable[[], float] = None

    def set_finalist(self):
        self._finalist = True

    def set_final_function(self, final_function: Callable[[], float]):
        self._final_function = final_function

    def reset(self):
        self._q = None
        self._f = None
        self._finalist = False

    @property
    def points(self) -> float:
        if self._q is None:
            self._q = self._qualify_points_function()

        return self._q

    @property
    def final(self) -> float:
        if self._f is None:
            self._f = self._final_function()

        return self._f

    @property
    def name(self):
        return self._name

    @property
    def nation(self):
        return self._nation

    def __lt__(self, other: Shooter) -> bool:
        if self._finalist:
            if self.final == other.final:
                return self.points < other.points
            return self.final < other.final

        return self.points < other.points


class Simulator:
    def __init__(self, shooters: List[Shooter]):
        self._shooters: List[Shooter] = shooters
        self._q: List[Shooter] = []
        self._finals: List[Shooter] = []

        for i in self._shooters:
            def func():
                prob = min(max(i.final_prob_function(), 0.1), 1)
                return np.random.binomial(40, prob, 1)
            i.set_final_function(partial(get_sample, func))

    @property
    def winners(self):
        return self._q

    def reset(self):
        self._finals = []
        self._q = []
        for i in self._shooters:
            i.reset()

            def func():
                prob = min(max(i.final_prob_function(), 0.1), 1)
                return np.random.binomial(40, prob, 1)
            i.set_final_function(partial(get_sample, func))

    def run(self):
        self._q = list(sorted(self._shooters, reverse=True))
        self._finals = self._q[:6]

        for i in self._finals:
            i.set_finalist()

        self._finals = list(sorted(self._finals, reverse=True))

        for n, i in enumerate(self._finals):
            self._q[n] = i
