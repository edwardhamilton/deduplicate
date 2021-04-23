import numpy as np
import pandas as pd
import geopandas
import statistics
import unittest
import math
import os
import sys
sys.path.append('../')
import loader
import filter


class Test_Filter(unittest.TestCase):
    def test_simple(self):
        df = loader.loader('name', 'platform', 'restaurant_id', sample = 10000).run(path = 'datasets', file = 'dataset1.csv', sep = chr(1))
        result = filter.filter(df, ngram_range=(1,3), min_name_vectorization_word_frequency=0.0, max_name_vectorization_word_frequency=.8,
            topn_by_cosine_similarity=20, min_cosine_similarity=.2, topn_matches_to_apply_model_to=500).run(df.index)

if __name__ == '__main__':
    unittest.main()
