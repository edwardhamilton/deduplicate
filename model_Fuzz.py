from fuzzywuzzy import fuzz
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score, KFold
import pandas as pd
import os
import utils
import numpy as np
import model

class model_Fuzz(model.model):
	def __init__(self, df, match_probability):
		super().__init__(df, match_probability)
	def predict(self, df):
		return (df.fuzz_ratio / 100.0).astype(float)    # fuzz_ratio is between 0 - 100 but predict_proba is between 0.0 and 1.0
	def get_features(self, left, right):
		lt, rt = self.map_indices_to_rows(left, right)
		ltName = lt.entity_name.replace('_', ' ')
		rtName = rt.entity_name.replace('_', ' ')
		fuzz_ratio = fuzz.ratio(ltName, rtName)
		return [fuzz_ratio]
	def add_features(self, df):
		def get_features(x):
			return self.get_features(x.left, x.right)
		return utils.apply(df, get_features, {'fuzz_ratio':int})
