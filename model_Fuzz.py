from fuzzywuzzy import fuzz
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score, KFold
import pandas as pd
import os
import utils
import numpy as np

class model_Fuzz:
	def __init__(self, df, match_probability):
		self.df = df
		self.match_probability = match_probability
	def map_indices_to_rows(self, x):
		return self.df.iloc[x.left], self.df.iloc[x.right]
	def predict(self, df): # df has 2 columns 'left' and 'right' which index into self.df
		if (df.empty):
			return df
		df = self.add_features(df)
		df['match'] = (df.fuzz_ratio / 100.0).astype(float)    # fuzz_ratio is between 0 - 100 but predict_proba is between 0.0 and 1.0
		df = df[df.match > self.match_probability]		# filter out bad matches
		return df
	def get_features(self, x):
		lt, rt = self.map_indices_to_rows(x)
		ltName = lt.entity_name.replace('_', ' ')
		rtName = rt.entity_name.replace('_', ' ')
		fuzz_ratio = fuzz.ratio(ltName, rtName)
		return [fuzz_ratio]
	def add_features(self, df):
		return utils.apply(df, self.get_features, {'fuzz_ratio':int})
