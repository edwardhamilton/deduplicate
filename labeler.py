class labeler:
	def __init__(self, args):
		self.args = args
		self.num_matches = 0
		self.num_notmatches = 0
		self.num_badrecords = 0
		self.false_positives = 0
		self.false_negatives = 0
		self.total_weight = 0.001
	def run(self):
		self.load_trainingset()
		self.generate_labeling_set()
		self.possible_matches = self.generate_labeling_set()
		self.num_possible_matches_left = self.possible_matches.shape[0]
		print('Begin labeling your training set (size = ' + str(self.possible_matches.shape[0]) + '):.  You will be prompted with possible matches.  Press (m) for match or (n) for not a match.  When done press (q)')
		self.labeled_pairs = set()

		for i, row in self.possible_matches.iterrows():
			left = int(row.left)
			right = int(row.right)
			if (self.pair_needs_labeling(left, right):
				self.present_pair_characteristics_to_user(left, right)
				self.get_label_from_user(row)
			else:
				self.num_possible_matches_left = self.num_possible_matches_left - 1

		print('Classification Model Error in (loaded) training set was: false positives = ' + str(int((false_positives * 100.0) / total_weight)) + '%' + ', False negatives = ' + str(int((false_negatives * 100.0) / total_weight)) + '%')
		print('Note: this is only classification modeling error.  Actual total error will be much lower.  However, each time we add more labels to the model, we hope that the error will decrease')
		print('Writing ' + str(tf.shape[0]) + ' labeled training data to ' + args.buildtrainset)
		tf.to_csv(os.path.join(args.path, args.buildtrainset), index=False)

	def create_labeled_training_row(match):
		return {'left': left, 'right': right, 'distance': distance, 'match':match}
	def label_match(self, row):
		self.num_matches = self.num_matches + 1
		weight = abs(self.config.match_probability - row.match)
		self.total_weight = self.total_weight + weight
		if (row.match < self.config.match_probability):
			self.false_negatives = self.false_negatives + weight
		self.tf = self.tf.append(self.create_labeled_training_row('T'), ignore_index=True)
		self.num_possible_matches_left = self.num_possible_matches_left - 1
		print('\t\t  ******* MATCH ************(' + str(self.num_matches) + ')\t\t\t\t' + str(self.num_possible_matches_left) + ' left: false negatives = ' + str(int((self.false_negatives * 100.0) / self.total_weight)) + '%')
	def label_notmatch(self, row):
		self.num_notmatches = num_notmatches + 1
		weight = abs(row.match - self.config.match_probability)
		self.total_weight = self.total_weight + weight
		if (row.match > self.config.match_probability):
			self.false_positives = self.false_positives + weight
		self.tf = self.tf.append(self.create_labeled_training_row('F'), ignore_index=True)
		self.num_possible_matches_left = self.num_possible_matches_left - 1
		print('\t\t  ------- NOT --------------(' + str(self.num_notmatches) + ')\t\t\t\t' + str(self.num_possible_matches_left) + ' left: false positives = ' + str(int((self.false_positives * 100.0) / self.total_weight)) + '%')
	def label_badrecord(self, row):
		self.num_badrecords = self.num_badrecords + 1
		self.num_possible_matches_left = self.num_possible_matches_left - 1
		print('\t\t  ------- BAD RECORD ------(' + str(self.num_bad_records) + ') -- NOT YET IMPLEMENTED\t\t\t\t' + str(self.num_possible_matches_left) + ' left')
	def load_trainingset(self)
		print('Building training set')
		self.tf = pd.DataFrame({'left':[], 'right':[], 'distance':[], 'match':[]})
		if (self.args.trainfile != None):
			temp = pd.read_csv(os.path.join(args.path, args.trainfile))
			for i in self.tf.columns:
				self.tf[i] = temp[i]
			print('Your starting training set already has ' + str(self.tf.shape[0]) + ' labeled match pairs.  You will add to this.')
		else:
			print('You are starting with fresh training set')
	def make_name_pair(left, right):
		return self.df.iloc[left].standardized_name + '.' + self.df.iloc[right].standardized_name

	def generate_labeling_set(self):
		print('First generate the set of possible matches that can be labelled')
		self.deduplicator = deduplicator(self.args)
		sample_save = args.sample
		args.sample = args.labeling_sample
		possible_matches = deduplicator.generate_matches()
		args.sample = sample_save   # make sure to put it back
		return possible_matches.sort_values(by=['match'])
	def pair_needs_labeling(self, left, right):
		return make_name_pair(left, right) in labeled_pairs) | (make_name_pair(right, left) in labeled_pairs) | (_df.iloc[left].standardized_name == _df.iloc[right].standardized_name)
	def present_pair_characteristics_to_user(self):
		booleanSameDict = {True: 'SAME', False: 'DIFFERENT'}
		distance, fuzz_ratio, fuzz_partial_ratio, fuzz_token_set_ratio, len_ratio, words_ratio, restaurantid_same, platform_same = self.model.get_match_features(left, right)
		self.labeled_pairs.add(make_name_pair(left, right))
		print('\tDistance = ' + str(distance) + 'm , RestaurantId = ' + booleanSameDict[restaurantid_same] + ', Platform = ' + booleanSameDict[platform_same] + ', Match = ' + str(int(row.match * 100.0)) + '%')
		print('\t' + _df.iloc[left].standardized_name.rjust(30) + '     <--->     ' + _df.iloc[right].standardized_name.ljust(30))

	def get_label_from_user(self, row):
		key = getch()
		if (key.lower() == b'm'):
			self.label_match(row)
		elif (key.lower() == b'n'):
			self.label_notmatch(row)
		elif (key.lower() == b'b'):
			self.label_badrecord(row)
		elif (key.lower() == b'q'):
			break
		else:
			print('Illegal key (' + str(key) + '): Press (m) for match or (n) for not a match.  When done press ENTER')
			num_possible_matches_left = num_possible_matches_left - 1
