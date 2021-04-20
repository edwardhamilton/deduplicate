class config(num_processes, region_division_size, max_region_span, max_region_size, topn_by_cosine_similarity, min_cosine_similarity, topn_matches_to_apply_model_to, max_match_distance, ngram_range, min_name_vectorization_word_frequency, max_name_vectorization_word_frequency, match_probability):
	def __init__(self, num_processes, region_division_size, max_region_span, max_region_size, topn_by_cosine_similarity, min_cosine_similarity, topn_matches_to_apply_model_to, max_match_distance, ngram_range, min_name_vectorization_word_frequency, max_name_vectorization_word_frequency, match_probability):
		if __name__ == '__main__':
			print(self)
		self.timeout = 10000
		self.max_region_span = max_region_span
		self.max_region_size = max_region_size
		self.region_division_size = region_division_size
		self.topn_by_cosine_similarity = topn_by_cosine_similarity
		self.min_cosine_similarity = min_cosine_similarity
		self.topn_matches_to_apply_model_to = topn_matches_to_apply_model_to
		self.max_match_distance = max_match_distance
		self.ngram_range = ngram_range
		self.min_name_vectorization_word_frequency = min_name_vectorization_word_frequency
		self.max_name_vectorization_word_frequency = max_name_vectorization_word_frequency
		self.match_probability = match_probability
	def __str__(self):
		return 	'Parameters: max_region_span = ' + str(self.max_region_span) + ', max_region_size = ' + str(self.max_region_size) + ', region_division_size = ' + str(self.region_division_size) + ', topn_by_cosine_similarity = ' + str(self.topn_by_cosine_similarity) 
				+ ', min_cosine_similarity = ' + str(self.min_cosine_similarity) + ', topn_matches_to_apply_model_to = ' + str(self.topn_matches_to_apply_model_to) + ', max_match_distance = ' + str(self.max_match_distance) 
				+ ', ngram(range)= ' + str(self.ngram_range) + ', min_name_vectorization_word_frequency = ' + str(self.min_name_vectorization_word_frequency)+ ', max_name_vectorization_word_frequency = ' + str(self.max_name_vectorization_word_frequency))
