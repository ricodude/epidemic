import enum
import math
import random


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
    def __init__(self, region, params, state=None):
        self._params = params
        self._sq_inf_dist = self._params['inf_dist'] ** 2
        self._region = region
        if state is None:
            self._state = State.SUSCEPTIBLE
        else:
            self._state = state
        self._duration = 0
        self._x_pos = random.random()
        self._y_pos = random.random()

        region.set_grid_pos(self, x_pos=self._x_pos, y_pos=self._y_pos)

    def remove(self):
        if self.is_infected():
            self._duration += 1
            if self._duration > self._params['inf_dur']:
                self._state = State.REMOVED

    def infect(self):
        if self.is_infected() and self._duration > 0:
            for ind in self.get_susceptible_neighbours():
                if ind.is_susceptible() and random.random() <= self._params['inf_prob']:
                    ind.set_infected()

    def move(self):
        old_x_pos = self._x_pos
        old_y_pos = self._y_pos
        theta = 2 * math.pi * random.random()
        self._x_pos = constrain(self._x_pos + math.sin(theta) * self._params['move_dist'], 0, 1)
        self._y_pos = constrain(self._y_pos + math.cos(theta) * self._params['move_dist'], 0, 1)
        self._region.update_grid_pos(self, old_x_pos=old_x_pos, old_y_pos=old_y_pos,
                                     new_x_pos=self._x_pos, new_y_pos=self._y_pos)

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

    def get_state(self):
        return self._state

    def get_susceptible_neighbours(self):
        neighbours = []
        for ind in self._region.get_possible_neighbours(self):
            if ind.is_susceptible() and self.sq_dist_from(ind) <= self._sq_inf_dist:
                neighbours.append(ind)
        return neighbours

    def sq_dist_from(self, ind):
        return sum([(x1 - x2) ** 2 for x1, x2 in zip(self.get_position(), ind.get_position())])


class Region:
    def __init__(self, num_individuals, params):
        self._params = params

        # Create a grid to optimise neighbour search
        self._grid_size = math.floor(1 / params['inf_dist'])
        self._grid = [[set() for _ in range(self._grid_size)] for _ in range(self._grid_size)]

        self._population = []
        # Add one infected individual
        self._population.append(Individual(self, state=State.INFECTED, params=params))
        # Rest are uninfected
        for _ in range(num_individuals - 1):
            self._population.append(Individual(self, params=params))

    def remove(self):
        for ind in self._population:
            ind.remove()

    def infect(self):
        for ind in self._population:
            ind.infect()

    def move(self):
        for ind in self._population:
            ind.move()

    def get_all_positions(self):
        pos_list = []
        for ind in self._population:
            pos_list.append(ind.get_position())
        return pos_list

    def get_population(self):
        return self._population

    def get_positions_for_state(self, state):
        pos_list = []
        for ind in self._population:
            if ind.is_in_state(state):
                pos_list.append(ind.get_position())
        return pos_list

    def get_possible_neighbours(self, ind):
        grid_x_pos, grid_y_pos = self.calc_grid_pos(*ind.get_position())
        offset_range = range(-1, 2)
        s = set()
        for i, j in [(i, j) for i in offset_range for j in offset_range]:
            check_grid_x_pos = constrain(grid_x_pos + i, 0, self._grid_size - 1)
            check_grid_y_pos = constrain(grid_y_pos + j, 0, self._grid_size - 1)
            s = s.union(self._grid[check_grid_x_pos][check_grid_y_pos])
        s.remove(ind)
        return s

    def get_state_counts(self):
        counts = {}
        for state in State:
            counts[state] = 0
        for ind in self._population:
            counts[ind.get_state()] += 1
        return counts

    def calc_grid_pos(self, x_pos, y_pos):
        return int(x_pos * self._grid_size), int(y_pos * self._grid_size)

    def set_grid_pos(self, ind, x_pos, y_pos):
        grid_x_pos, grid_y_pos = self.calc_grid_pos(x_pos, y_pos)
        self._grid[grid_x_pos][grid_y_pos].add(ind)

    def unset_grid_pos(self, ind, x_pos, y_pos):
        grid_x_pos = int(x_pos * self._grid_size)
        grid_y_pos = int(y_pos * self._grid_size)
        self._grid[grid_x_pos][grid_y_pos].remove(ind)

    def update_grid_pos(self, ind, old_x_pos, old_y_pos, new_x_pos, new_y_pos):
        old_grid_x_pos, old_grid_y_pos = self.calc_grid_pos(old_x_pos, old_y_pos)
        new_grid_x_pos, new_grid_y_pos = self.calc_grid_pos(new_x_pos, new_y_pos)
        if new_grid_x_pos != old_grid_x_pos or new_grid_y_pos != old_grid_y_pos:
            self._grid[old_grid_x_pos][old_grid_y_pos].remove(ind)
            self._grid[new_grid_x_pos][new_grid_y_pos].add(ind)


class Simulation:
    DEFAULT_PARAMS = {
        'inf_dist': 0.03,
        'inf_dur': 14,
        'inf_prob': 0.2,
        'move_dist': 0.01,
    }

    def __init__(self, num_individuals, params=None):
        random.seed(0)
        self._params = self.DEFAULT_PARAMS
        if params is not None:
            for k, v in params.items():
                self._params[k] = v
        self._region = Region(num_individuals, params=self._params)

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

    def get_all_positions(self):
        return self._region.get_all_positions()

    def get_population_size(self):
        return len(self._region.get_population())

    def get_positions_for_state(self, state):
        return self._region.get_positions_for_state(state)

    def get_state_counts(self):
        return self._region.get_state_counts()
