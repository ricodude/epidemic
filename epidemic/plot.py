import matplotlib.pyplot as plt
import numpy as np

import epidemic.simulation as es

STATE_COLORS = {
    es.State.INFECTED: 'red',
    es.State.REMOVED: 'gray',
    es.State.SUSCEPTIBLE: 'blue',
}
INITIAL_LINE_RANGE = 100


class SimPlotter:
    def __init__(self, sim, pause=0.1):
        self._sim = sim
        self._pause = pause
        plt.ion()
        self._fig = plt.figure(figsize=(15, 5))

        self._ax_scatter = self._fig.add_axes([0.03, 0.1, 0.27, 0.8])
        self._ax_scatter.set_xlim(0, 1)
        self._ax_scatter.set_ylim(0, 1)

        self._ax_line = self._fig.add_axes([0.35, 0.1, 0.63, 0.8])
        self._ax_line.set_xlim(0, INITIAL_LINE_RANGE)
        self._ax_line.set_ylim(0, sim.get_population_size())

        self._line_values = {state: [count] for state, count in self._sim.get_state_counts().items()}
        self._line_infected, = self._ax_line.plot([0], self._line_values[es.State.INFECTED], c='red', label='Infected')
        self._line_removed, = self._ax_line.plot([0], self._line_values[es.State.INFECTED], c='gray', label='Removed')
        self._ax_line.legend(loc='upper left')

        self._update_lines = True

        self._state_scatters = {}

        self.plot()

    def run(self, num_steps=None):
        step = 0
        self.plot()
        while num_steps is None or step < num_steps:
            plt.pause(self._pause)
            self.step()
            step += 1

    def step(self):
        self._sim.step()
        self.plot()

    def plot(self):
        for state in es.State:
            self.plot_scatter_for_state(state)

        if self._update_lines:
            for state, count in self._sim.get_state_counts().items():
                self._line_values[state].append(count)
                if state == es.State.INFECTED and count == 0:
                    self._update_lines = False

            self.plot_line_for_state(es.State.INFECTED)
            self.plot_line_for_state(es.State.REMOVED)

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

    def plot_line_for_state(self, state):
        # TODO: This is ugly
        if state == es.State.INFECTED:
            line = self._line_infected
        else:
            line = self._line_removed

        y_vals = self._line_values[state]
        x_vals = range(len(y_vals))

        self._ax_line.set_xlim(0, max(INITIAL_LINE_RANGE, len(y_vals)))

        line.set_xdata(x_vals)
        line.set_ydata(y_vals)
