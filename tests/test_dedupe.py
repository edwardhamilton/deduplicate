import numpy as np
import pandas as pd
import geopandas
import statistics
import unittest
import math
import sys
import helpers
import os
sys.path.append('../')
import dedupe
import utils
import loader
import partition
import match
import parallelize
import filter_Distance
import filter_TfidfCosSimilar_and_Distance
import model_Fuzz
import model_Xgboost

class Test_Dedupe(unittest.TestCase):
    @utils.ignore_warnings
    def setUp(self):
        self.df = helpers.load_dataset()
        self.filter = filter_TfidfCosSimilar_and_Distance.filter_TfidfCosSimilar_and_Distance(self.df, ngram_range=(1,4), min_name_vectorization_word_frequency=0.0,
            max_name_vectorization_word_frequency=.8, topn_by_cosine_similarity=30,
            min_cosine_similarity=.2, topn_matches_to_apply_model_to=1000, max_distance=150)
        self.model = model_Xgboost.model_Xgboost(self.df, match_probability = .5, path = 'datasets', train_file = 'trainset.csv')
        self.match = match.match(self.filter, self.model)
        self.partition = partition.partition(data=self.df, divisor=4, max_span=50, max_size=2000)
    @utils.ignore_warnings
    def __test_generate_matches(self):
        job = utils.sample_index(self.df, sample=1000)
        matches = parallelize.parallelize(num_processes=1, map=self.partition, reduce=self.match).run(job)
    @utils.ignore_warnings
    def __test_without_training(self):
        result = dedupe.dedupe(data=self.df, partition=self.partition, match=self.match).run(num_processes=1, sample=None)
    @utils.ignore_warnings
    def test_with_training_full(self):
        result = dedupe.dedupe(data=self.df, partition=self.partition, match=self.match).run(num_processes=1, sample=None)
        result.to_csv(os.path.join('datasets', 'output_1.csv'), index=False)   # prevent overwrite previous file



if __name__ == '__main__':
    unittest.main()
