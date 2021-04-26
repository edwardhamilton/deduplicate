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
import model_Fuzz
import model_Xgboost
import utils


class Test_Model(unittest.TestCase):
    @utils.ignore_warnings
    def setUp(self):
        self.df, self.possible_matches = helpers.load_filtered_dataset()
    @utils.ignore_warnings
    def test_Fuzz(self):
        model = model_Fuzz.model_Fuzz(self.df, match_probability = .5)
        prediction = model.predict(self.possible_matches)
    @utils.ignore_warnings
    def __test_Xgboost(self):
        model = model_Xgboost.model_Xgboost(self.df, match_probability = .5)
        prediction = model.predict(self.possible_matches)
        model.train(path = 'datasets', file = 'trainset.csv')
        prediction = model.predict(self.possible_matches)


if __name__ == '__main__':
    unittest.main()
