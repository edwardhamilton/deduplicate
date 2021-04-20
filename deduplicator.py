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
	def prepare_data():
		self.clean_and_remove_inactive()
		self.clean_longitude_latitude()
		self.df = self.df.reset_index(drop=True)  #so index has now holes
		self.simple_standardization_ofnames()
		self.gdf = geopandas.GeoDataFrame(self.df, geometry=geopandas.points_from_xy(df.longitude, df.latitude))
	def clean_and_remove_inactive():
		boolMap = {True : True, False : False, 'TRUE': True, 'True': True, 'FALSE': False, 'False': False}
		print('Dropping ' + str(len(df[df['active'].isin(boolMap.keys()) == False])) + ' records due to bad active status')
		df.drop(df[df['active'].isin(boolMap.keys()) == False].index, inplace = True)
		df.active = _df.active.map(boolMap)
		df.drop(df[df['active'] == False].index, inplace = True)

	def clean_longitude_latitude():
		df.longitude = pd.to_numeric(_df.longitude, errors='coerce')
		df.latitude = pd.to_numeric(_df.latitude, errors='coerce')
		outofrange = -1000
		df.longitude = df.longitude.fillna(outofrange)
		df.latitude = df.latitude.fillna(outofrange)
		to_drop_because_latitude_outofrange = df[is_outofrange(-90, 90, df['latitude'])]
		to_drop_because_longitude_outofrange = df[is_outofrange(-180, 180, df['longitude'])]
		print('Dropping ' + str(len(to_drop_because_latitude_outofrange) + len(to_drop_because_longitude_outofrange)) + ' longitude/latitude out of range')
		df.drop(df[is_outofrange(-90, 90, df['latitude'])].index, inplace = True)
		df.drop(df[is_outofrange(-180, 180, df['longitude'])].index, inplace = True)

	def simple_standardization_ofnames():
		_words_to_remove = ['restaurant', 'catering', 'bar', 'cuisine']
		regexNonChars = re.compile('[^a-zA-Z0-9]+')
		def clean_name(name):
			token_separator = ' '
			result = name
			result = result.lower()
			for w in _words_to_remove:	 					# remove unhelpful words
				result = result.replace(w, '')
			result = re.sub("[\(\[].*?[\)\]]", "", result)  # usually addresses or comments are within parenthesis
			i = result.find('-') 							# usually comments or address come after '-', so we get rid of them
			if (i > 0):
				result = result[0:i]
			result = regexNonChars.sub(token_separator, result)   		# replace non alphanum with '_'
			if result.endswith(token_separator):  						# get rid of '_' at ends
				result = result[:-1]
			if result.startswith(token_separator): 						# get rid of '_' at ends
				result = result[-1:]
			return result
		df.entity_name = df[args.entity_name].apply(lambda x: clean_name(x))
		print('Simple standardization reduced from ' + str(len(df.name.unique())) + ' to ' + str(len(df.standardized_name.unique())) + ' unique names')
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
	def assign_clusters(matches):
		df = self.df
		print('Assign clusters from matches')
		matches_df = pd.DataFrame(data = matches, columns = ['cluster', 'to', 'match'])  			# since the match pairs are order (lowest number first) we can use the 'left' side as a cluster id
		matches_df = matches_df.reset_index().sort_values(by=['to','cluster']).set_index('to')   	# we want to ['to', 'cluster'] but duplicates checked on 'to' only.   Then next line makes sure only first is kept
		matches_df = matches_df[~matches_df.index.duplicated()]   									# given [1 -> 2 ] and [3 -> 2 ] there should exists a [1 -> 3] as well.  So if we remove all duplicates (keeping the first - sorted by smallest) this should give us what we want
		# Note: while dropping the duplicate of [1 -> 7], and [3 -> 7] becoming [1 -> 7] would seem like a problem, because matching is symetric, there must also be a [3 -> 1] (which becomes [1 -> 3] (via order_pair) and so 3 joins the cluster
																	
		print(str(matches_df.shape[0]) + ' matches left after merging into clusters: at ' + str(time.perf_counter()))
		matches_df = matches_df.reset_index()

		# assign cluster id to each cluster
		df['cluster'] = df.index  # by default each record belongs to its own cluster
		matches_df = matches_df.set_index('to')
		df.update(matches_df['cluster'])
		
		# assign average match probability per cluster
		df['match'] = 1.0			# each record matches with itself with 100% probability.  If a record is a member of a cluster then it will be assigned average value for its cluster
		clusterMatch = matches_df.groupby('cluster').apply(lambda group: statistics.mean(group['match'])).reset_index()
		clusterMatch.columns = ['cluster', 'match']
		df.set_index('cluster', inplace=True)
		df.update(clusterMatch.set_index('cluster'))
		df.reset_index(inplace=True)
		
		
		# set cluster size.  This may help with QA.  Find large clusters easily

		df['cluster_temp'] = df['cluster']  
		cluster_size_df = df.cluster_temp.value_counts().rename_axis('cluster_temp').reset_index(name='cluster_size')
		df = df.set_index('cluster_temp').join(cluster_size_df.set_index('cluster_temp'))
		df = df.sort_values(by=['cluster_size', 'cluster'], ascending=False)  # its convenient to have largest clusters first when opening in excel
		df['match'] = (df['match'] * 100).astype(int)		# easier to filter (in excel) when % are integers
		print('Final # record = ' + str(df.shape[0]) + ', Unique clusters = ' + str(len(df.cluster.unique())) + ', at ' + str(time.perf_counter()))
