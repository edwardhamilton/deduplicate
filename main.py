
class main():
	def __init__():
		pass
	def run(self):
		args = get_commandline_args()
		set_default_config(args)
		if __name__ == '__main__':
			deduplicator = deduplicator(args)
			if args.buildtrainset is not None:
				build_trainset(args)
				print('Now run deduplicate with new training set')
				deduplicate(args, train_file=args.buildtrainset)
			else:
				deduplicate(args, args.trainfile)
			_df.drop(['geom', 'geometry'], inplace = True, axis = 1)
			_df.to_csv(os.path.join(args.path, 'output_' + str(time.perf_counter()) + '.csv'), index=False)   # prevent overwrite previous file

	def set_default_config(args):
		set_config(
			num_processes = args.processes, 				# None means not multiprocessing.   I'm not confident about the multiprocessing.  I don't fully understand its behavior
			region_division_size = 10, 						# regions are divided is into 10x10 grids (and then futher divided), until max_region_span and max_region_size constraints are met
			max_region_span = 100,  						# km.    We generally want to match on records nearby.    There's a balance between too many regions (performance) and too large regions (quality)
			max_region_size=5000,							# Top n from Cosine Similarity is used to filter matches.   If it is applied to too many records then good potential matches are not seen.
			topn_by_cosine_similarity = 20, 				# Used by Cosine Similarity filter
			min_cosine_similarity = 0.2, 					# Used by Cosine Similarity filter
			topn_matches_to_apply_model_to = 5000,			# Consider these many matches from Cosine Similarity filter
			max_match_distance = args.max_match_distance, 	# 150 meters should cover GPS error
			ngram_range=(1,3), 								# Name vectorization
			min_name_vectorization_word_frequency = 0.0,    # Name vectorization, If this is constraining, then we might get an exception for small regions.  If exception triggers, it removes the constraint and tries again.
			max_name_vectorization_word_frequency = .8, 	# Name vectorization. If this is constraining, then we might get an exception for small regions.  If exception triggers, it removes the constraint and tries again.
			match_probability = args.match_probability		# this might be useful for testing as we could set the probably below 50% and see if we catch any more matches.
			)

	def get_commandline_args():
		parser = argparse.ArgumentParser(description='Generate clusters for records that represent the same business entity (using cosine similarity and distance as filters, and then sending resultant pairs through classification model)'
			+ '\n\tIf --trainfile is not supplied then it will use simple string matching '
			+ '\n\tTo build --trainfile specify --buildtrainset.  It will initially run the matching algorithm without model to generate random set of samples that model would see, and allow user to label samples (match or not match)',
			formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument('--path', required = True, type=pathlib.Path, help='working directory.  All filenames are relative to this path')
		parser.add_argument('--runfile', required = True, help='the is the file that will be deduplicated')
		parser.add_argument('--buildtrainset', required = False, help='indicates to build training set, and indicates the output filename')
		parser.add_argument('--trainfile', required = False, help='file to be used for training model, must have been pregenerated with --train command')
		parser.add_argument('--processes', required = False, type=int, default=0, help='use multiple processes.  Not fully tested')
		parser.add_argument('--max_match_distance', required = False, type=int, default=150, choices=[range(0, 1000)], help='records more than this meters apart will not be considered for matching')
		parser.add_argument('--match_probability', required = False, type=float, default=.5, choices=[Range(0.0, 1.0)], help='records with match probability greater than this value will be matched')
		parser.add_argument('--sample', required = False, type=int, help='limit deduplicate to a sample of entire set.  samples are randomized')
		parser.add_argument('--labeling_sample', required = False, type=int, help='you may need to pretty large sample to get a good set of possible matches for labelling.')
		args = parser.parse_args()
		return args
