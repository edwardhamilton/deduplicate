class match:
    def __init__(self, filter, model):
        self.filter = filter
        self.model = model
		matches = []
		self.parent = parent
		if ((len(indices) > 1)): # & False): # no need to check if region only has 1 item
			logging.info('matching region = ' + str(len(indices)) + ', shape_gdf = ' + str(_gdf.shape))
			matches = get_matches(region)
		else:
			logging('partition has only 1 element so matching not needed ')
		logging.info('adding to results: partition = ' + str(len(indices)) + ', # matches = ' + str(len(matches)))
		self.result = (indices, matches)

	def get_matches(self, indices):
        matches = []
		if ((len(indices) > 1)): # & False): # no need to check if region only has 1 item
			logging.info('matching region = ' + str(len(indices)) + ', shape_gdf = ' + str(_gdf.shape))
            indices = np.array(indices)
            matches_df = self.model.predict_matches(self.filter.run(indices))
		    matches = matches_df[['left', 'right', 'match']].values.tolist()
		else:
			logging('partition has only 1 element so matching not needed ')
		logging.info('adding to results: partition = ' + str(len(indices)) + ', # matches = ' + str(len(matches)))
		return (indices, matches)
