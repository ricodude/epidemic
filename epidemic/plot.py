import matplotlib.pyplot as plt
import numpy as np

import epidemic.simulation as es

STATE_COLORS = {
    es.State.INFECTED: 'red',
    es.State.REMOVED: 'gray',
    es.State.SUSCEPTIBLE: 'blue',
}
INITIAL_LINE_RANGE = 100


class SimAxesPlotter:
    def __init__(self, sim, fig, plot_scale, x_scale, y_scale, x_offset, y_offset):
        self._sim = sim
        self._plot_scale = plot_scale

        self._ax_scatter = fig.add_axes([0.03 * x_scale + x_offset, 0.1 * y_scale + y_offset,
                                         0.27 * x_scale, 0.8 * y_scale])
        self._ax_scatter.set_xlim(0, 1)
        self._ax_scatter.set_ylim(0, 1)

        self._ax_line = fig.add_axes([0.35 * x_scale + x_offset, 0.1 * y_scale + y_offset,
                                      0.63 * x_scale, 0.8 * y_scale])
        self._ax_line.set_xlim(0, INITIAL_LINE_RANGE)
        self._ax_line.set_ylim(0, sim.get_population_size())

        self._line_values = {state: [count] for state, count in self._sim.get_state_counts().items()}
        self._line_infected, = self._ax_line.plot([0], self._line_values[es.State.INFECTED], c='red', label='Infected')
        self._line_removed, = self._ax_line.plot([0], self._line_values[es.State.INFECTED], c='gray',
                                                 label='Removed + Infected')
        self._ax_line.legend(loc='upper left')

        self._update_lines = True

        self._state_scatters = {}

    def step(self):
        self._sim.step()

    def plot(self):
        for state in es.State:
            self.plot_scatter_for_state(state)

        state_counts = self._sim.get_state_counts()
        if self._update_lines:
            self._line_values[es.State.INFECTED].append(state_counts[es.State.INFECTED])
            self._line_values[es.State.REMOVED].append(state_counts[es.State.REMOVED] +
                                                       state_counts[es.State.INFECTED])
            if state_counts[es.State.INFECTED] == 0:
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
            new_sc = self._ax_scatter.scatter(*np.array(list(zip(*positions))),
                                              s=18 * (self._plot_scale ** 2),
                                              c=STATE_COLORS[state], alpha=0.5)
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
    SINGLE_PLOT_WIDTH = 12
    SINGLE_PLOT_HEIGHT = 4
    MAX_HEIGHT = 12
    HEIGHT_STACK = 5

    def __init__(self, sim_or_sim_list,
                 single_plot_width=SINGLE_PLOT_WIDTH, single_plot_height=SINGLE_PLOT_HEIGHT,
                 max_height=MAX_HEIGHT, height_stack=HEIGHT_STACK):
        if hasattr(sim_or_sim_list, '__iter__'):
            self._sim_list = sim_or_sim_list
        else:
            self._sim_list = [sim_or_sim_list]

        # Figure out how many plots high & wide - and the corresponding scaling factors
        num_sims = len(self._sim_list)
        x_num = 1 + int((num_sims - 1) / height_stack)
        x_scale = 1 / x_num
        y_num = min(height_stack, num_sims)
        y_scale = 1 / y_num

        # Set the height & width for the figure accordingly
        unadj_height = y_num * single_plot_height
        fig_height = min(unadj_height, max_height)
        plot_scale = fig_height / unadj_height
        fig_width = x_num * single_plot_width * plot_scale

        plt.ion()

        self._fig = plt.figure(figsize=(fig_width, fig_height))

        self._sap_list = []
        for i, sim in enumerate(self._sim_list):
            x_pos, y_pos = divmod(i, height_stack)
            x_offset = x_pos * x_scale
            y_offset = (y_num - y_pos - 1) * y_scale
            self._sap_list.append(SimAxesPlotter(sim, fig=self._fig, plot_scale=plot_scale, x_scale=x_scale,
                                                 y_scale=y_scale, x_offset=x_offset, y_offset=y_offset))

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
