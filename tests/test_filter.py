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


class Test_Filter(unittest.TestCase):
    @utils.ignore_warnings
    def test_simple(self):
        helpers.load_filtered_dataset()  # just testing that it doesn't crash
if __name__ == '__main__':
    unittest.main()
