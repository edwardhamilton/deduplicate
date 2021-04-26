import pandas as pd
import numpy as np
import itertools
import utils


class filter_Distance:  # generates a set of possible matches
    def __init__(self, df, max_distance):
        self.df = df
        self.max_distance = max_distance
    def get_distance(self, x):
        return [utils.get_distance(self.df.iloc[x.left], self.df.iloc[x.right])]
    def add_distance(self, df):
        return utils.apply(df, self.get_distance, {'distance':float})
    def filter_bydistance(self, data):
        df = pd.DataFrame(data=data, columns = ['left', 'right'])
        df.left = df.left.astype(int)
        df.right = df.right.astype(int)
        df = self.add_distance(df)
        df = df[df.distance < self.max_distance]		# filter out bad matches
        df = df.drop(['distance'], axis = 1)
        return df[['left', 'right']]

    def run(self, indices):
        return self.filter_bydistance(itertools.combinations(indices, 2))
