import numpy as np
import pandas as pd
import geopandas
import statistics
import unittest
import math
import os
import sys
import helpers
sys.path.append('../')
import utils
import filter_Distance


class Test_Filter(unittest.TestCase):
    @utils.ignore_warnings
    def test_TfidfCosSimilar_and_Distance(self):
        df, filtered = helpers.load_filtered_dataset()  # just testing that it doesn't crash
        print(filtered)
    @utils.ignore_warnings
    def __test_Distance(self):
        df, filtered = helpers.load_filtered_dataset()  # just testing that it doesn't crash
        filtered = filter_Distance.filter_Distance(df, max_distance=15000000).run(df.sample(10).index)
        print(filtered)


if __name__ == '__main__':
    unittest.main()
