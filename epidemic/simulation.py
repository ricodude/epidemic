import enum
import math
import random

import matplotlib as mpl


def constrain(val, min_val, max_val):
    if val < min_val:
        return max_val - min_val + val
    elif val > max_val:
        return min_val + max_val - val
    else:
        return val


class State(enum.Enum):
    SUSCEPTIBLE = 1
    INFECTED = 2
    REMOVED = 3


class Individual:
    def __init__(self, state=None):
        if state is None:
            self._state = State.SUSCEPTIBLE
        else:
            self._state = state
        self._x_pos = random.random()
        self._y_pos = random.random()

    def move(self):
        theta = 2 * math.pi * random.random()
        self._x_pos = constrain(self._x_pos + math.sin(theta) / 100, 0, 1)
        self._y_pos = constrain(self._y_pos + math.cos(theta) / 100, 0, 1)


class Space:
    def __init__(self, num_individuals):
        self._population = []
        for i in range(num_individuals):
            self._population.append(Individual())

    def move(self):
        for i in self._population:
            i.move()


class Simulation:
    def __init__(self, num_individuals):
        self._space = Space(num_individuals)

    def step(self):
        self._space.move()
