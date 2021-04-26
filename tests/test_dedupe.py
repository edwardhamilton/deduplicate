import numpy as np
import pandas as pd
import geopandas
import statistics
import unittest
import math
import sys
import helpers

sys.path.append('../')
import dedupe
import utils
import loader
import model
import partition
import match
import parallelize


class Test_Dedupe(unittest.TestCase):
    @utils.ignore_warnings
    def setUp(self):
        self.df = helpers.load_dataset()
        self.filter = helpers.create_filter(self.df)
        self.model = model.model(self.df, match_probability = .5)
        self.match = match.match(self.filter, self.model)
        self.partition = partition.partition(data=self.df, divisor=4, max_span=50, max_size=1000)
    @utils.ignore_warnings
    def __test_generate_matches(self):
        job = utils.sample_index(self.df, sample=1000)
        matches = parallelize.parallelize(num_processes=1, map=self.partition, reduce=self.match).run(job)
    @utils.ignore_warnings
    def __test_without_training(self):
        self.model.train(path = 'datasets', file = 'trainset.csv')
        result = dedupe.dedupe(data=self.df, partition=self.partition, match=self.match).run(num_processes=1, sample=None)
    @utils.ignore_warnings
    def test_with_training_full(self):
        self.model.train(path = 'datasets', file = 'trainset.csv')
        result = dedupe.dedupe(data=self.df, partition=self.partition, match=self.match).run(num_processes=1, sample=None)


if __name__ == '__main__':
    unittest.main()
