import numpy as np
import pandas as pd
import unittest
import math

import sys
import helpers

sys.path.append('../')
import utils
import cluster


class Test_Cluster(unittest.TestCase):
    @utils.ignore_warnings
    def test_simple(self):
        num_clusters=10
        df, matches = helpers.generate_random_match_pairs(size=1000, num_clusters=num_clusters)
        __cluster = cluster.cluster(data=df, cluster='left', to='right', match='match')
        result = __cluster.run(matches)
        self.assertEqual(len(result['cluster'].unique()), num_clusters)

if __name__ == '__main__':
    unittest.main()
