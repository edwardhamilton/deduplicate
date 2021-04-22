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


class Test_Loader(unittest.TestCase):
    def test_simple(self):
        __loader = loader.loader('name', 'platform', 'restaurant_id')
        df = __loader.run(path = 'datasets', file = 'dataset1.csv', sep = chr(1))
        self.assertEqual(len(df.standardized_name.unique()), 210267)
        self.assertEqual(df.shape[0], 568803)
        self.assertEqual(df.shape[1], 14)


if __name__ == '__main__':
    unittest.main()
