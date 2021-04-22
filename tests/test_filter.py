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
        __loader = loader.loader('name', 'platform', 'restaurant_id', sample = 10000)
        df = __loader.run(path = 'datasets', file = 'dataset1.csv', sep = chr(1))
        ngram_range=(1,3)                                # Name vectorization
        min_name_vectorization_word_frequency = 0.0      # Name vectorization, If this is constraining, then we might get an exception for small regions.  If exception triggers, it removes the constraint and tries again.
        max_name_vectorization_word_frequency = .8       # Name vectorization. If this is constraining, then we might get an exception for small regions.  If exception triggers, it removes the constraint and tries again.
        topn_by_cosine_similarity = 20  				 # Used by Cosine Similarity filter
        min_cosine_similarity = 0.2  					 # Used by Cosine Similarity filter
        topn_matches_to_apply_model_to = 500 			 # Consider these many matches from Cosine Similarity filter
        __filter = filter.filter(df, ngram_range, min_name_vectorization_word_frequency, max_name_vectorization_word_frequency, topn_by_cosine_similarity, min_cosine_similarity, topn_matches_to_apply_model_to)
        result = __filter.run(df.index)

if __name__ == '__main__':
    unittest.main()
