import pandas as pd
class model:
	def __init__(self, df, match_probability):
		self.df = df
		self.match_probability = match_probability
	def map_indices_to_rows(self, left, right):
		return self.df.iloc[left], self.df.iloc[right]
	def run(self, matches): # df has 2 columns 'left' and 'right' which index into self.df
		if (len(matches) == 0):
			return []
		df = self.add_features(pd.DataFrame(data=matches, columns = { 'left', 'right'}))
		df['match'] = self.predict(df)
		df = df[df.match > self.match_probability]		# filter out bad matches
		return df[['left', 'right', 'match']].values.tolist()
	def predict(self, df):
		raise NotImplementedError
	def add_features(self, df):
		raise NotImplementedError
