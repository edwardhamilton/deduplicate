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
