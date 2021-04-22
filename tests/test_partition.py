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


class Test_Partition(unittest.TestCase):
    def setUp(self):
        self.size = 1000
        self.data = { 'id': list(range(0, self.size)), 'lng' : list(utils.randfloat(-90, 90, size = self.size)),  'lat' : list(utils.randfloat(-180, 180, size = self.size)) }
        self.df = pd.DataFrame(self.data)
        self.gdf = geopandas.GeoDataFrame(self.df, geometry=geopandas.points_from_xy(self.df.lng, self.df.lat))
    def __test_partition(self, divisor):
        partitions = partition.partition(gdf=self.gdf, divisor=divisor, max_span=1000000000, max_size=10).run(self.gdf.index)
        self.assertEqual(len(partitions), math.pow(divisor, 2))
        unique_records = set(list(np.concatenate(partitions).flat))
        self.assertEqual(len(unique_records), self.size)
    def test_numpartitionscorrect_and_allrecordsincludedonce(self):
        self.__test_partition(divisor=2)
        self.__test_partition(divisor=4)
        self.__test_partition(divisor=10)

if __name__ == '__main__':
    unittest.main()
