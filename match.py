class match:
    def __init__(self, context, region):
		matches = []
		self.parent = parent
		if ((len(region) > 1)): # & False): # no need to check if region only has 1 item
			trace('matching region = ' + str(len(region)) + ', shape_gdf = ' + str(_gdf.shape))
			matches = get_matches(region)
		else:
			trace('region has only 1 element so matching not needed ')
		trace('adding to results: region = ' + str(len(region)) + ', # matches = ' + str(len(matches)))
		self.result = (region, matches)

	def order_pair(left, right):  # this makes it easier to assign cluster id, as first in match pair.
		if (left <= right):
			return left, right
		return right, left
	def filter(self, indices):
		gdf = self.context.gdf.iloc[indices]
		try:  # name vectorization
			tfidf_vectorizer = TfidfVectorizer(ngram_range=context.config.ngram_range, max_df=context.config.max_name_vectorization_word_frequency, min_df=context.config.min_name_vectorization_word_frequency, token_pattern='(\S+)')
			tf_idf_matrix = tfidf_vectorizer.fit_transform(gdf[self.context.entity_name])
		except: # relax constraints and try again
			tfidf_vectorizer = TfidfVectorizer(ngram_range=_ngram_range, max_df=1.0, min_df=0, token_pattern='(\S+)')
			tf_idf_matrix = tfidf_vectorizer.fit_transform(gdf[self.context.entity_name])
		sparse_matrix = awesome_cossim_topn(tf_idf_matrix, tf_idf_matrix.transpose(), context.config.topn_by_cosine_similarity, context.config.min_cosine_similarity)
		non_zeros = sparse_matrix.nonzero()
		top_n_rows = min(context.config.topn_matches_to_apply_model_to, sparsecols.size)
		return pd.DataFrame(data=np.dstack((indices[non_zeros[0][:top_n_rows]], non_zeros[1][:top_n_rows]))[0], columns = ['left', 'right'])
	def get_matches(self, indices):
		indices = np.array(indices)
		matches_df = self.predict_matches(self.filter(indices))
		return matches_df[['left', 'right', 'match']].values.tolist()
