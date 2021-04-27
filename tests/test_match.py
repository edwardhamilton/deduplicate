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
import filter_Distance
import filter_TfidfCosSimilar_and_Distance
import model_Fuzz
import model_Xgboost
import match
import utils


class Test_Match(unittest.TestCase):
    @utils.ignore_warnings
    def setUp(self):
        self.df = helpers.load_dataset()
    @utils.ignore_warnings
    def test_CosSimilar_Xgboost(self):
        filter = filter_TfidfCosSimilar_and_Distance.filter_TfidfCosSimilar_and_Distance(self.df, ngram_range=(1,3), min_name_vectorization_word_frequency=0.0,
            max_name_vectorization_word_frequency=.8, topn_by_cosine_similarity=20,
            min_cosine_similarity=.2, topn_matches_to_apply_model_to=1000, max_distance=150)
        model = model_Xgboost.model_Xgboost(self.df, match_probability = .5, path = 'datasets', train_file = 'trainset.csv')
        print(match.match(filter, model).run(self.df.sample(10000).index))
    @utils.ignore_warnings
    def test_Distance_Fuzz(self):
        filter = filter_Distance.filter_Distance(self.df, max_distance=15000000)
        model = model_Fuzz.model_Fuzz(self.df, match_probability = .5)
        print(match.match(filter, model).run(self.df.sample(100).index))

if __name__ == '__main__':
    unittest.main()
