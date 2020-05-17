import unittest

import epidemic.plot as ep
import epidemic.simulation as es


class TestSimulation(unittest.TestCase):
    def test_one_step(self):
        # GIVEN
        sim = es.Simulation(1000)
        plotter = ep.SimPlotter(sim)

        # WHEN
        plotter.step()

        # THEN
        self.assertTrue(True)

    def test_10_plots(self):
        # GIVEN
        sim = es.Simulation(1000)
        plotter = ep.SimPlotter(sim)

        # WHEN
        plotter.run(num_steps=10)

        # THEN
        self.assertTrue(True)

    def test_100_plots(self):
        # GIVEN
        sim = es.Simulation(100)
        plotter = ep.SimPlotter(sim, pause=0.01)

        # WHEN
        plotter.run(num_steps=100)

        # THEN
        self.assertTrue(True)
