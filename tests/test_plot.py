import unittest

import epidemic.plot as ep
import epidemic.simulation as es


class TestSimulation(unittest.TestCase):
    def test_one_step(self):
        sim = es.Simulation(1000)
        plotter = ep.SimPlotter(sim)
        plotter.step()
        self.assertTrue(True)

    def test_10_plots(self):
        sim = es.Simulation(1000)
        plotter = ep.SimPlotter(sim)
        plotter.plot(num_steps=10)
        self.assertTrue(True)

    def test_100_plots(self):
        sim = es.Simulation(1000)
        plotter = ep.SimPlotter(sim)
        plotter.plot(num_steps=100)
        self.assertTrue(True)
