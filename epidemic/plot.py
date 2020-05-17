import matplotlib.pyplot as plt
import numpy as np

import epidemic.simulation as es

STATE_COLORS = {
    es.State.INFECTED: 'red',
    es.State.REMOVED: 'gray',
    es.State.SUSCEPTIBLE: 'blue',
}


class SimPlotter:
    def __init__(self, sim, pause=0.1):
        self._sim = sim
        self._pause = pause
        plt.ion()
        self._fig = plt.figure(figsize=(15, 5))
        self._ax_scatter = self._fig.add_axes([0.03, 0.1, 0.27, 0.8])
        self._ax_line = self._fig.add_axes([0.33, 0.1, 0.63, 0.8])
        self._state_scatters = {}

    def run(self, num_steps=None):
        step = 0
        while num_steps is None or step < num_steps:
            plt.pause(self._pause)
            self.step()
            step += 1

    def step(self):
        self._sim.step()
        for state in es.State:
            self.plot_scatter_for_state(state)

    def plot_scatter_for_state(self, state):
        positions = self._sim.get_positions_for_state(state)
        if state in self._state_scatters:
            if len(positions) > 0:
                self._state_scatters[state].set_offsets(np.array(positions))
            else:
                sc = self._state_scatters.pop(state)
                sc.remove()
        elif len(positions) > 0:
            new_sc = self._ax_scatter.scatter(*np.array(list(zip(*positions))), c=STATE_COLORS[state], alpha=0.5)
            self._state_scatters[state] = new_sc
