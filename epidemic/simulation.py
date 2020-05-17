import enum
import math
import random

INFECTION_DISTANCE = 0.03
INFECTION_DURATION = 14
INFECTION_PROBABILITY = 0.25
MOVE_DISTANCE = 0.01

SQ_INFECTION_DISTANCE = INFECTION_DISTANCE ** 2


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
    def __init__(self, region, state=None):
        self._region = region
        if state is None:
            self._state = State.SUSCEPTIBLE
        else:
            self._state = state
        self._duration = 0
        self._x_pos = random.random()
        self._y_pos = random.random()

    def remove(self):
        if self.is_infected():
            self._duration += 1
            if self._duration > INFECTION_DURATION:
                self._state = State.REMOVED

    def infect(self):
        if self.is_infected() and self._duration > 0:
            for ind in self.get_susceptible_neighbours():
                if ind.is_susceptible() and random.random() <= INFECTION_PROBABILITY:
                    ind.set_infected()

    def move(self):
        theta = 2 * math.pi * random.random()
        self._x_pos = constrain(self._x_pos + math.sin(theta) / 100, 0, 1)
        self._y_pos = constrain(self._y_pos + math.cos(theta) / 100, 0, 1)

    def is_infected(self):
        return self._state == State.INFECTED

    def is_removed(self):
        return self._state == State.REMOVED

    def is_susceptible(self):
        return self._state == State.SUSCEPTIBLE

    def is_in_state(self, state):
        return self._state == state

    def set_infected(self):
        self._state = State.INFECTED

    def get_position(self):
        return self._x_pos, self._y_pos

    def get_susceptible_neighbours(self):
        neighbours = []
        for ind in self._region.get_population():
            if ind != self and ind.is_susceptible() and self.sq_dist_from(ind) <= SQ_INFECTION_DISTANCE:
                neighbours.append(ind)
        return neighbours

    def sq_dist_from(self, ind):
        return sum([(x1 - x2) ** 2 for x1, x2 in zip(self.get_position(), ind.get_position())])


class Region:
    def __init__(self, num_individuals):
        self._population = []
        # Add one infected individual
        self._population.append(Individual(self, state=State.INFECTED))
        # Add one removed individual
        self._population.append(Individual(self, state=State.REMOVED))
        # Rest are uninfected
        for _ in range(num_individuals - 2):
            self._population.append(Individual(self))

    def remove(self):
        for ind in self._population:
            ind.remove()

    def infect(self):
        for ind in self._population:
            ind.infect()

    def move(self):
        for ind in self._population:
            ind.move()

    def get_positions_for_state(self, state):
        pos_list = []
        for ind in self._population:
            if ind.is_in_state(state):
                pos_list.append(ind.get_position())
        return pos_list

    def get_all_positions(self):
        pos_list = []
        for ind in self._population:
            pos_list.append(ind.get_position())
        return pos_list

    def get_population(self):
        return self._population


class Simulation:
    def __init__(self, num_individuals):
        self._region = Region(num_individuals)

    def step(self):
        self.remove()
        self.infect()
        self.move()

    def remove(self):
        self._region.remove()

    def infect(self):
        self._region.infect()

    def move(self):
        self._region.move()

    def get_positions_for_state(self, state):
        return self._region.get_positions_for_state(state)

    def get_all_positions(self):
        return self._region.get_all_positions()
