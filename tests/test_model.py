import numpy as np
import pandas as pd
import geopandas
import statistics
import unittest
import math
import sys
import helpers
sys.path.append('../')
import loader
import filter
import model
import utils


class Test_Model(unittest.TestCase):
    @utils.ignore_warnings
    def setUp(self):
        self.df, self.possible_matches = helpers.load_filtered_dataset()
        self.model = model.model(self.df, match_probability = .5)
    @utils.ignore_warnings
    def test_without_training(self):
        prediction = self.model.predict(self.possible_matches)
    @utils.ignore_warnings
    def __test_with_training(self):
        self.model.train(path = 'datasets', file = 'trainset.csv')
        prediction = self.model.predict(self.possible_matches)


if __name__ == '__main__':
    unittest.main()
