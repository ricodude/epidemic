import unittest

import epidemic.simulation as es


class TestSimulation(unittest.TestCase):
    def test_one_step(self):
        # GIVEN
        simul = es.Simulation(100)

        # WHEN
        simul.step()

        # THEN
        self.assertTrue(True)


    def test_many_steps(self):
        # GIVEN
        simul = es.Simulation(1000)

        # WHEN
        for _ in range(1000):
            simul.step()

        # THEN
        self.assertTrue(True)
