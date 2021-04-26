from fuzzywuzzy import fuzz
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score, KFold
import pandas as pd
import os
import utils
import numpy as np

class predict:  # this is a reduce that returns full prediction information (with features).  Maybe be useful for debugging
	def __init__(self, filter, model):
		self.filter = filter
		self.model = model
	def run(self, indices):
		if ((len(indices) > 1)): # & False): # no need to check if region only has 1 item
			indices = np.array(indices)
			if (self.filter != None):
				filtered = self.filter.run(indices)
			else:
				filtered = indices
			matches_df = self.model.predict(filtered)
			if (matches_df.shape[0] > 0):
				return matches_df
		return None
class model:
	def __init__(self, df, match_probability):
		self.df = df
		self.match_probability = match_probability
		self.xgbc = None
	def predict(self, df): # df has 2 columns 'left' and 'right' which index into self.df
		if (df.empty):
			return df
		df = self.add_features(df)
		if (self.xgbc != None):
			X = model.get_X(df)
			df['match'] = self.xgbc.predict_proba(X).T[1].astype(float)
		else:
			df['match'] = (df.fuzz_ratio / 100.0).astype(float)    # fuzz_ratio is between 0 - 100 but predict_proba is between 0.0 and 1.0
		df = df[df.match > self.match_probability]		# filter out bad matches
		return df
	def get_features(self, x):
		left = x.left
		right = x.right
		df = self.df
		lt = df.iloc[left]
		rt = df.iloc[right]
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
		return df[['distance', 'fuzz_ratio', 'fuzz_partial_ratio', 'fuzz_token_set_ratio', 'len_ratio', 'words_ratio', 'entityid_same', 'platform_same']]
	def train(self, path, file):
		self.xgbc = XGBClassifier()
		print('Training prediction model on file ' + str(file))
		tf = pd.read_csv(os.path.join(path, file))
		tf.drop('distance', axis=1, inplace = True)
		tf = self.add_features(tf)
		tf.match = (tf.match == 'T').astype(bool)
		X = model.get_X(tf)
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
