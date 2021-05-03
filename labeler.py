import pandas as pd
import os
from enum import Enum, auto
class LABEL(Enum):
	MATCH = auto()
	NOT_MATCH = auto()
	BAD_RECORD = auto()
	QUIT = auto()
	ERROR = auto()

class pair_labeler:
	def __init__(self, model):
		self.model = model
	def run(self, left, right, match):  #labeled_pairs is list of pairs already labeled once we consider a pair we want to add it here
		raise NotImplementedError


class labeler:
	def __init__(self, num_processes, data, dedupe, pair_labeler, path, train_file, sample):
		self.num_processes, self.df, self.dedupe, self.pair_labeler, self.path, self.train_file, self.sample = num_processes, data, dedupe, pair_labeler, path, train_file, sample
		self.pair_labeler.parent = self
		self.num_matches = 0
		self.num_notmatches = 0
		self.num_badrecords = 0
		self.false_positives = 0
		self.false_negatives = 0
		self.total_weight = 0.001
		self.match_probability = self.dedupe.match.model.match_probability
	def load_trainingset(self):
		print('Building training set')
		self.tf = pd.DataFrame({'left':[], 'right':[], 'distance':[], 'match':[]})
		if (self.train_file != None):
			temp = pd.read_csv(os.path.join(self.path, self.train_file))
			for i in self.tf.columns:
				self.tf[i] = temp[i]
			print('Your starting training set already has ' + str(self.tf.shape[0]) + ' labeled match pairs.  You will add to this.')
		else:
			print('You are starting with fresh training set')
	def generate_labeling_set(self):
		print('First generate the set of possible matches that can be labelled')
		result = self.dedupe.get_matches(num_processes=self.num_processes, sample=self.sample)
		possible_matches = pd.DataFrame(data = result, columns = ['left', 'right', 'match'])  			# since the match pairs are order (lowest number first) we can use the 'left' side as a cluster id
		return possible_matches.sort_values(by=['match'])
	def run(self):
		self.load_trainingset()
		self.possible_matches = self.generate_labeling_set()
		self.num_possible_matches_left = self.possible_matches.shape[0]
		print('Begin labeling your training set (size = ' + str(self.possible_matches.shape[0]) + '):.  You will be prompted with possible matches.  Press (m) for match or (n) for not a match.  When done press (q)')
		self.labeled_pairs = set()

		for i, row in self.possible_matches.iterrows():
			left = int(row.left)
			right = int(row.right)
			if (self.pair_needs_labeling(left, right)):
				print('pair needs labeling')
				if (self.label_row(left, right, row.match) == False):
					print('done')
					break; # done
			else:
				self.num_possible_matches_left = self.num_possible_matches_left - 1

		print('Classification Model Error in (loaded) training set was: false positives = ' + str(int((self.false_positives * 100.0) / self.total_weight)) + '%' + ', False negatives = ' + str(int((self.false_negatives * 100.0) / self.total_weight)) + '%')
		print('Note: this is only classification modeling error.  Actual total error will be much lower.  However, each time we add more labels to the model, we hope that the error will decrease')
		print('Writing ' + str(self.tf.shape[0]) + ' labeled training data to ' + self.train_file)
		self.tf.to_csv(os.path.join(self.path, self.train_file), index=False)

	def get_label(self, left, right):
		raise NotImplementedError

	def label_row(self, left, right, match):
		label = self.pair_labeler.run(left, right, match)
		if (label == LABEL.MATCH):
			self.label_match(match)
		elif (label == LABEL.NOT_MATCH):
			self.label_notmatch(match)
		elif (label == LABEL.BAD_RECORD):
			self.label_badrecord(match)
		elif (label == LABEL.QUIT):
			return False
		elif (label == LABEL.ERROR):
			self.num_possible_matches_left = self.num_possible_matches_left - 1
		return True

	def create_labeled_training_row(match):
		return {'left': left, 'right': right, 'distance': distance, 'match':match}
	def label_match(self, match):
		self.num_matches = self.num_matches + 1
		weight = abs(self.match_probability - match)
		self.total_weight = self.total_weight + weight
		if (match < self.match_probability):
			self.false_negatives = self.false_negatives + weight
		self.tf = self.tf.append(self.create_labeled_training_row('T'), ignore_index=True)
		self.num_possible_matches_left = self.num_possible_matches_left - 1
		print('\t\t  ******* MATCH ************(' + str(self.num_matches) + ')\t\t\t\t' + str(self.num_possible_matches_left) + ' left: false negatives = ' + str(int((self.false_negatives * 100.0) / self.total_weight)) + '%')
	def label_notmatch(self, row, match):
		self.num_notmatches = num_notmatches + 1
		weight = abs(match - self.dedupe.match_probability)
		self.total_weight = self.total_weight + weight
		if (match > self.match_probability):
			self.false_positives = self.false_positives + weight
		self.tf = self.tf.append(self.create_labeled_training_row('F'), ignore_index=True)
		self.num_possible_matches_left = self.num_possible_matches_left - 1
		print('\t\t  ------- NOT --------------(' + str(self.num_notmatches) + ')\t\t\t\t' + str(self.num_possible_matches_left) + ' left: false positives = ' + str(int((self.false_positives * 100.0) / self.total_weight)) + '%')
	def label_badrecord(self, row, match):
		self.num_badrecords = self.num_badrecords + 1
		self.num_possible_matches_left = self.num_possible_matches_left - 1
		print('\t\t  ------- BAD RECORD ------(' + str(self.num_bad_records) + ') -- NOT YET IMPLEMENTED\t\t\t\t' + str(self.num_possible_matches_left) + ' left')
	def make_name_pair(self, left, right):
		return self.df.iloc[left].standardized_name + '.' + self.df.iloc[right].standardized_name

	def pair_needs_labeling(self, left, right):
		return (self.make_name_pair(left, right) in self.labeled_pairs) | (self.make_name_pair(right, left) in self.labeled_pairs) | (self.df.iloc[left].standardized_name == self.df.iloc[right].standardized_name)
