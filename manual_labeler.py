from getch import getch, pause
import labeler
import model

class manual_labeler(labeler.pair_labeler):
	def __init__(self, model):
		super().__init__(model)
	def run(self, left, right, match):
		print('label manually')
		self.present_pair_characteristics_to_user(left, right, match)
		return self.get_label_from_user()
	def present_pair_characteristics_to_user(self, left, right, match):
		booleanSameDict = {True: 'SAME', False: 'DIFFERENT'}
		distance, fuzz_ratio, fuzz_partial_ratio, fuzz_token_set_ratio, len_ratio, words_ratio, restaurantid_same, platform_same = self.model.get_features(left, right)
		self.parent.labeled_pairs.add(self.parent.make_name_pair(left, right))
		print('\tDistance = ' + str(distance) + 'm , RestaurantId = ' + booleanSameDict[restaurantid_same] + ', Platform = ' + booleanSameDict[platform_same] + ', Match = ' + str(int(match * 100.0)) + '%')
		print('\t' + self.parent.df.iloc[left].standardized_name.rjust(30) + '     <--->     ' + self.parent.df.iloc[right].standardized_name.ljust(30))
	def get_label_from_user(self):
		key = getch()
		if (key.lower() == b'm'):
			return labeler.LABEL.MATCH
		elif (key.lower() == b'n'):
			return labeler.LABEL.NOT_MATCH
		elif (key.lower() == b'b'):
			return labeler.LABEL.BAD_RECORD
		elif (key.lower() == b'q'):
			return labeler.LABEL.QUIT
		else:
			print('Illegal key (' + str(key) + '): Press (m) for match or (n) for not a match.  When done press ENTER')
			num_possible_matches_left = num_possible_matches_left - 1
