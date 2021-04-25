from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
import sparse_dot_topn.sparse_dot_topn as ct
from sparse_dot_topn import awesome_cossim_topn
import pandas as pd
import numpy as np

class filter:
    def __init__(self, df, ngram_range, min_name_vectorization_word_frequency, max_name_vectorization_word_frequency, topn_by_cosine_similarity, min_cosine_similarity, topn_matches_to_apply_model_to):
        self.df = df
        self.ngram_range = ngram_range
        self.max_name_vectorization_word_frequency = max_name_vectorization_word_frequency
        self.min_name_vectorization_word_frequency = min_name_vectorization_word_frequency
        self.topn_by_cosine_similarity = topn_by_cosine_similarity
        self.min_cosine_similarity = min_cosine_similarity
        self.topn_matches_to_apply_model_to = topn_matches_to_apply_model_to
    def run(self, indices):
        df = self.df.iloc[indices]
        try:  # name vectorization
            tfidf_vectorizer = TfidfVectorizer(ngram_range=self.ngram_range, max_df=self.max_name_vectorization_word_frequency, min_df=self.min_name_vectorization_word_frequency, token_pattern='(\S+)')
            tf_idf_matrix = tfidf_vectorizer.fit_transform(df.standardized_name)
        except: # relax constraints and try again
            tfidf_vectorizer = TfidfVectorizer(ngram_range=self.ngram_range, max_df=1.0, min_df=0, token_pattern='(\S+)')
            tf_idf_matrix = tfidf_vectorizer.fit_transform(df.standardized_name)
        sparse_matrix = awesome_cossim_topn(tf_idf_matrix, tf_idf_matrix.transpose(), self.topn_by_cosine_similarity, self.min_cosine_similarity)
        non_zeros = sparse_matrix.nonzero()
        sparserows = non_zeros[0]
        sparsecols = non_zeros[1]
        top_n_rows = min(self.topn_matches_to_apply_model_to, sparsecols.size)
        df = pd.DataFrame(data=np.dstack((indices[non_zeros[0][:top_n_rows]], non_zeros[1][:top_n_rows]))[0], columns = ['left', 'right'])
        df.left = df.left.astype(int)
        df.right = df.right.astype(int)
        return df
