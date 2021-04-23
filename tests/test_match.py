import numpy as np
import pandas as pd
import geopandas
import statistics
import unittest
import math

import sys
sys.path.append('../')
import loader
import filter
import model
import match
import utils


class Test_Match(unittest.TestCase):
    def setUp(self):
        self.df = loader.loader('name', 'platform', 'restaurant_id').run(path = 'datasets', file = 'dataset1.csv', sep = chr(1))
        self.filter = filter.filter(self.df, ngram_range=(1,3), min_name_vectorization_word_frequency=0.0, max_name_vectorization_word_frequency=.8,
            topn_by_cosine_similarity=20, min_cosine_similarity=.2, topn_matches_to_apply_model_to=500)
        # we need full dataset for model as that's what training set is based on
        self.model = model.model(self.df, match_probability = .5)
        self.match = match.match(self.filter, self.model)
    def test_without_training(self):
        matches = self.match.run(self.df.sample(10000).index)
    def test_with_training(self):
        self.model.train(path = 'datasets', file = 'trainset.csv')
        matches = self.match.run(self.df.sample(10000).index)

if __name__ == '__main__':
    unittest.main()
