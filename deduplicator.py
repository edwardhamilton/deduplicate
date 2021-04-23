class deduplicator:
	class context:
		def __init__(self):
			pass
		def initialize(self, args, df, model):
			self.args = args
			self.df = df
			self.model = model

	def __init__(self, args)
		self.args = args
		self.context = context()

	def run(self):  #assigns a same cluster # to records that are the same business entity
		assign_cluster(self.generate_matches())
	def generate_matches(self):
		self.df = pd.read_csv(os.path.join(self.args.path, self.args.runfile), sep = chr(1))
		self.model = model(self.context)
		self.context = context.initialize(self.args, self.df, self.model)
		self.prepare_data()   # cleaning up and some preprocessing
		if (self.args.train_file != None):
			self.model.train(self.args, self.args.train_file) # indices must match between run file and train file
		print('Starting matching on ' + str(len(entired_region)) + ' records, using prediction model at ' + str(time.perf_counter()))
		job = list(if (args.sample != None) gdf.sample(args.sample).index else gdf.index))
		return collect_matches(parallelize(context, partition, match, job).results)
	def collect_matches(results):
		print('Aggregating results: ' + str(len(results)))

		matches = []  # aggregating all items before clustering might allow us to merge when logical cluster cross multiple regions (todo)
		unique_regions = set()
		regions = []
		results = []
		# empty the results queue and then kill processes
		def get_region_size(r):
			return len(r[0])
		def get_num_region_matches(r):
			return len(r[1])
		def get_matches(r):
			return r[1]
		def get_num_region_matches(r):
			return len(r[1])
		print('Matches stats:')
		print('\t# regions = ' + str(len(results)) + ', # records = ' + str(sum(list(map(get_region_size, results)))) + ', Region Size: Avg = ' + str(statistics.mean(list(map(get_region_size, results)))) + ', Min = ' + str(min(list(map(get_region_size, results)))) + ', Max = ' + str(max(list(map(get_region_size, results)))))
		print('\tTotal matches = ' + str(sum(list(map(get_num_region_matches, results)))) + ', By Region: Avg = ' + str(statistics.mean(list(map(get_num_region_matches, results)))) + ', Min = ' + str(min(list(map(get_num_region_matches, results)))) + ', Max = ' + str(max(list(map(get_num_region_matches, results)))))

		try:
			matches = list(np.concatenate(list(filter(lambda x: x, list(map(get_matches, results))))))  # note: empty list gets evaludated to false
		except:  # in case no matches
			pass
		print('Worker processes terminated: Matches = ' + str(len(matches)) + ', at ' + str(time.perf_counter()))
		return matches
