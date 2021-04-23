import parallelize
import numpy as np

class dedupe:
	# data has already been cleaned
	def __init__(self, data, partition, match):
		self.df = data
		self.partition = partition_size
		self.match = match
	def run(self, sample = None):  #assigns a same cluster # to records that are the same business entity
		job = list(self.df.sample(sample).index if (sample != None) else self.df.index)
		return collect_matches(cluster(self.df, cluster='cluster', to='to', match='match').run(parallelize(partition, match).run(job)))
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
