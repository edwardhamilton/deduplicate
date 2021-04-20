class model:
	def __init__(self, context):
		self.context = context
		self.xgbc = XGBClassifier()
	def predict_matches(self, df):
		df = df.add_features(df)
		if (self.xgbc != None):
			X = get_X(df)
			df.match = self.xgbc.predict_proba(X).T[1].astype(float)
		else:
			df.match = (df.fuzz_ratio / 100.0).astype(float)    # fuzz_ratio is between 0 - 100 but predict_proba is between 0.0 and 1.0
		df.match = df[df.match > self.context.config.match_probability]		# filter out bad matches
		return df
	def get_match_features(self, x):
		left = x.left
		right = x.right
		gdf = self.context.gdf
		lt = gdf.iloc[left]
		rt = gdf.iloc[right]
		distance = get_distance(lt, rt)
		ltName = lt.entity_name.replace('_', ' ')
		rtName = rt.entity_name.replace('_', ' ')
		fuzz_ratio = fuzz.ratio(ltName, rtName)
		fuzz_partial_ratio = fuzz.partial_ratio(ltName, rtName)
		fuzz_token_set_ratio = fuzz.token_set_ratio(ltName, rtName)
		len_ratio = abs(len(ltName) - len(rtName)) / max(len(ltName), len(rtName))
		words_ratio = abs((ltName.count(' ') + 1) - (rtName.count(' ') + 1)) / max(ltName.count(' ') + 1, rtName.count(' ') + 1)
		entityid_same = lt.entity_id == rt.entity_id
		platform_same = lt.platform == rt.platform
		return distance, fuzz_ratio, fuzz_partial_ratio, fuzz_token_set_ratio, len_ratio, words_ratio, restaurantid_same, platform_same
	def add_features(df):
		return df.merge(df.apply(lambda x: self.get_match_features), left_index=True, right_index=True)
	def get_X(df):
		return df[['distance', 'fuzz_ratio', 'fuzz_partial_ratio', 'fuzz_token_set_ratio', 'len_ratio', 'words_ratio', 'entityid_same', 'platform_same']]
	def train(self, file):
		print('Training prediction model on file ' + str(file))
		tf = pd.read_csv(os.path.join(self.context.args.path, file))
		tf = self.add_features(tf)
		tf.match = (tf.match == 'T').astype(bool)
		X = get_X(tf)
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
