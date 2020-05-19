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

    def test_10_steps(self):
        # GIVEN
        sim = es.Simulation(1000)
        plotter = ep.SimPlotter(sim)

        # WHEN
        plotter.run(num_steps=10)

        # THEN
        self.assertTrue(True)

    def test_2_sims(self):
        # GIVEN
        sim_list = [es.Simulation(100) for _ in range(2)]
        plotter = ep.SimPlotter(sim_list)

        # WHEN
        plotter.run(num_steps=10)

        # THEN
        self.assertTrue(True)

    def test_3_sims(self):
        # GIVEN
        sim_list = [es.Simulation(100) for _ in range(3)]
        plotter = ep.SimPlotter(sim_list)

        # WHEN
        plotter.run(num_steps=10)

        # THEN
        self.assertTrue(True)

    def test_4_sims(self):
        # GIVEN
        sim_list = [es.Simulation(100) for _ in range(4)]
        plotter = ep.SimPlotter(sim_list)

        # WHEN
        plotter.run(num_steps=10)

        # THEN
        self.assertTrue(True)
