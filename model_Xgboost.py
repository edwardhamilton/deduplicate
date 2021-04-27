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

class model_Xgboost(model.model):
	def __init__(self, df, match_probability, path, train_file):
		super().__init__(df, match_probability)
		self.train(path, train_file)
	def predict(self, df):
		try:
			X = model_Xgboost.get_X(df)
			return self.xgbc.predict_proba(X).T[1].astype(float)
		except:
			print('catch: 1')
			return 0.0
	def get_features(self, x):
		lt, rt = super().map_indices_to_rows(x)
		distance = utils.get_distance(lt, rt)
		ltName = lt.entity_name.replace('_', ' ')
		rtName = rt.entity_name.replace('_', ' ')
		fuzz_ratio = fuzz.ratio(ltName, rtName)
		fuzz_partial_ratio = fuzz.partial_ratio(ltName, rtName)
		fuzz_token_set_ratio = fuzz.token_set_ratio(ltName, rtName)
		len_ratio = abs(len(ltName) - len(rtName)) / max(len(ltName), len(rtName))
		words_ratio = abs((ltName.count(' ') + 1) - (rtName.count(' ') + 1)) / max(ltName.count(' ') + 1, rtName.count(' ') + 1)
		entityid_same = lt.entity_id == rt.entity_id
		platform_same = lt.platform == rt.platform
		return [distance, fuzz_ratio, fuzz_partial_ratio, fuzz_token_set_ratio, len_ratio, words_ratio, entityid_same, platform_same]
	def add_features(self, df):
		return utils.apply(df, self.get_features, {'distance':float, 'fuzz_ratio':int, 'fuzz_partial_ratio':int, 'fuzz_token_set_ratio':int, 'len_ratio':float, 'words_ratio':float, 'entityid_same':bool, 'platform_same':bool})
	def get_X(df):
		try:
			return df[['distance', 'fuzz_ratio', 'fuzz_partial_ratio', 'fuzz_token_set_ratio', 'len_ratio', 'words_ratio', 'entityid_same', 'platform_same']]
		except:
			print('catch5')
			return pd.DataFrame({'distance':[], 'fuzz_ratio':[], 'fuzz_partial_ratio':[], 'fuzz_token_set_ratio':[], 'len_ratio':[], 'words_ratio':[], 'entityid_same':[], 'platform_same':[]})
	def train(self, path, file):
		self.xgbc = XGBClassifier()
		print('Training prediction model on file ' + str(file))
		tf = pd.read_csv(os.path.join(path, file))
		tf.drop('distance', axis=1, inplace = True)
		tf = self.add_features(tf)
		tf.match = (tf.match == 'T').astype(bool)
		X = model_Xgboost.get_X(tf)
		y = tf.match
		Xtrain, Xtest, ytrain, ytest=train_test_split(X, y, test_size=0.15)
		self.xgbc.fit(Xtrain, ytrain)
		scores = cross_val_score(self.xgbc, Xtrain, ytrain, cv=5)
		print("\tMean cross-validation score: %.2f" % scores.mean())
		kfold = KFold(n_splits=10, shuffle=True)
		kf_cv_scores = cross_val_score(self.xgbc, Xtrain, ytrain, cv=kfold)
		print("\tK-fold CV average score: %.2f" % kf_cv_scores.mean())
		ypred = self.xgbc.predict(Xtest)
		print(confusion_matrix(ytest, ypred))
