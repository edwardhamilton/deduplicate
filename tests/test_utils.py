import numpy as np
import pandas as pd
import geopandas
import statistics
import unittest
import math

import sys
sys.path.append('../')
import partition
import utils


class Test_Utils(unittest.TestCase):
    def test_isoutofrange(self):
        self.assertTrue(utils.is_outofrange(10, 20, 30))
        self.assertFalse(utils.is_outofrange(10, 20, 15))

if __name__ == '__main__':
    unittest.main()
