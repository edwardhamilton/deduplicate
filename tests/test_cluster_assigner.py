import numpy as np
import pandas as pd
import unittest
import math
from random import random

import sys
sys.path.append('../')
import utils
import cluster_assigner

class Test_ClusterAssigner(unittest.TestCase):
    def test_simple(self):
        df = pd.DataFrame({ 'cluster_id' : np.random.randint(low=1, high=10, size=100) })
        df['id'] = df.index
        df = df.set_index('cluster_id').join(df.set_index('cluster_id'), lsuffix='_left', rsuffix='_right')
        df.rename(columns={'id_left': 'left'}, inplace=True)
        df.rename(columns={'id_right': 'right'}, inplace=True)
        df.reset_index(inplace=True)
        df.drop(df[df.left == df.right].index, inplace = True)
        df.left, df.right = np.where(random() > .5, [df.right, df.left], [df.left, df.right])   # randomly swap left and right.
        df['match'] = .5
        df = df.astype({'cluster_id':int, 'left':int, 'right':int, 'match':float })
        matches = df[['left', 'right', 'match']].values.tolist()
        __cluster_assigner = cluster_assigner.cluster_assigner(df, 'left', 'right', 'match')
        result = __cluster_assigner.run(matches)

if __name__ == '__main__':
    unittest.main()
