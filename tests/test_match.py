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
import match
import utils


class Test_Match(unittest.TestCase):
    @utils.ignore_warnings
    def setUp(self):
        self.df = helpers.load_dataset()
        self.filter = helpers.create_filter(self.df)
        self.model = model.model(self.df, match_probability = .5)
        self.match = match.match(self.filter, self.model)
    @utils.ignore_warnings
    def test_without_training(self):
        matches = self.match.run(self.df.sample(10000).index)
    @utils.ignore_warnings
    def test_with_training(self):
        self.model.train(path = 'datasets', file = 'trainset.csv')
        matches = self.match.run(self.df.sample(10000).index)

if __name__ == '__main__':
    unittest.main()
