import unittest
import numpy as nps

from src.services.DendriteFractal import DendriteFractal


class DedriteFractalTest(unittest.TestCase):

    def __init__(self):
        self.dendrite_fractal = DendriteFractal(-1.188, 0.305)
        self.dendrite_fractal.generate_julia_set()

    def generate_julia_set_test(self):
        data = self.generate_julia_set_test()
        x = np.linespace()

        self.assertEqual(data,expected_data)