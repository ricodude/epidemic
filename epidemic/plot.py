import matplotlib.pyplot as plt
import numpy as np

import epidemic.simulation as es

SIM_PLOT_WIDTH = 12
SIM_PLOT_HEIGHT = 4

STATE_COLORS = {
    es.State.INFECTED: 'red',
    es.State.REMOVED: 'gray',
    es.State.SUSCEPTIBLE: 'blue',
}
INITIAL_LINE_RANGE = 100


class SimAxesPlotter:
    def __init__(self, sim, fig, y_scale, y_offset):
        self._sim = sim

        self._ax_scatter = fig.add_axes([0.03, 0.1 * y_scale + y_offset, 0.27, 0.8 * y_scale])
        self._ax_scatter.set_xlim(0, 1)
        self._ax_scatter.set_ylim(0, 1)

        self._ax_line = fig.add_axes([0.35, 0.1 * y_scale + y_offset, 0.63, 0.8 * y_scale])
        self._ax_line.set_xlim(0, INITIAL_LINE_RANGE)
        self._ax_line.set_ylim(0, sim.get_population_size())

        self._line_values = {state: [count] for state, count in self._sim.get_state_counts().items()}
        self._line_infected, = self._ax_line.plot([0], self._line_values[es.State.INFECTED], c='red', label='Infected')
        self._line_removed, = self._ax_line.plot([0], self._line_values[es.State.INFECTED], c='gray', label='Removed')
        self._ax_line.legend(loc='upper left')

        self._update_lines = True

        self._state_scatters = {}

    def step(self):
        self._sim.step()

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


class SimPlotter:
    def __init__(self, sim_or_sim_list):
        if hasattr(sim_or_sim_list, '__iter__'):
            self._sim_list = sim_or_sim_list
        else:
            self._sim_list = [sim_or_sim_list]

        plt.ion()

        num_sims = len(self._sim_list)
        if num_sims <= 3:
            fig_width = SIM_PLOT_WIDTH
            fig_height = num_sims * SIM_PLOT_HEIGHT
        else:
            fig_width = SIM_PLOT_WIDTH * 3 / num_sims
            fig_height = 3 * SIM_PLOT_HEIGHT

        self._fig = plt.figure(figsize=(fig_width, fig_height))

        self._sap_list = []
        y_scale = 1 / num_sims
        for i, sim in enumerate(self._sim_list):
            self._sap_list.append(SimAxesPlotter(sim, fig=self._fig, y_scale=y_scale, y_offset=i * y_scale))

        self.plot()

    def run(self, num_steps=None, pause=0.1):
        step = 0
        while num_steps is None or step < num_steps:
            plt.pause(pause)
            self.step()
            step += 1

    def step(self):
        for sap in self._sap_list:
            sap.step()
        self.plot()

    def plot(self):
        for sap in self._sap_list:
            sap.plot()
