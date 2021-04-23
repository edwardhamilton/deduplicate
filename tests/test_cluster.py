import numpy as np
import pandas as pd
import unittest
import math

import sys
sys.path.append('../')
import utils
import cluster

class Test_Cluster(unittest.TestCase):
    def __generate_matches(self, df):
        matches_df = df.set_index('cluster_id').join(df.set_index('cluster_id'), lsuffix='_left', rsuffix='_right')
        matches_df.rename(columns={'id_left': 'left'}, inplace=True)
        matches_df.rename(columns={'id_right': 'right'}, inplace=True)
        matches_df.reset_index(inplace=True)
        matches_df.drop(matches_df[matches_df.left == matches_df.right].index, inplace = True)
        utils.swap_columns_randomly(matches_df, 'left', 'right')          # make sure solution is order independent
        matches_df['match'] = .5
        matches_df = matches_df.astype({'cluster_id':int, 'left':int, 'right':int, 'match':float })
        return matches_df[['left', 'right', 'match']].values.tolist()

    def test_simple(self):
        num_clusters = 10
        df = pd.DataFrame({ 'cluster_id' : np.random.randint(low=0, high=num_clusters, size=1000) })
        df['id'] = df.index
        matches = self.__generate_matches(df)
        __cluster = cluster.cluster(data=df, cluster='left', to='right', match='match')
        result = __cluster.run(matches)
        self.assertEqual(len(result['cluster'].unique()), num_clusters)

if __name__ == '__main__':
    unittest.main()
