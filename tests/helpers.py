import numpy as np
import pandas as pd
import math

import sys
sys.path.append('../')
import utils
import loader
import filter

def generate_random_match_pairs(size, num_clusters):
    df = pd.DataFrame({ 'cluster_id' : np.random.randint(low=0, high=num_clusters, size=size) })
    df['id'] = df.index
    matches_df = df.set_index('cluster_id').join(df.set_index('cluster_id'), lsuffix='_left', rsuffix='_right')
    matches_df.rename(columns={'id_left': 'left'}, inplace=True)
    matches_df.rename(columns={'id_right': 'right'}, inplace=True)
    matches_df.reset_index(inplace=True)
    matches_df.drop(matches_df[matches_df.left == matches_df.right].index, inplace = True)
    utils.swap_columns_randomly(matches_df, 'left', 'right')          # make sure solution is order independent
    matches_df['match'] = .5
    matches_df = matches_df.astype({'cluster_id':int, 'left':int, 'right':int, 'match':float })
    return df, matches_df[['left', 'right', 'match']].values.tolist()
def load_dataset():
    return loader.loader('name', 'platform', 'restaurant_id').run(path = 'datasets', file = 'dataset1.csv', sep = chr(1))

def create_filter(df):
    return filter.filter(df, ngram_range=(1,3), min_name_vectorization_word_frequency=0.0,
        max_name_vectorization_word_frequency=.8, topn_by_cosine_similarity=20,
        min_cosine_similarity=.2, topn_matches_to_apply_model_to=500)

def load_filtered_dataset():
    df = load_dataset()
    filtered = create_filter(df).run(df.sample(10000).index)
    return df, filtered
