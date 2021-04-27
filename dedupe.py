import numpy as np
import statistics
import parallelize
import cluster
import utils

class dedupe:
	# data has already been cleaned
	def __init__(self, data, partition, match):
		self.df = data
		self.partition = partition
		self.match = match
	def run(self, num_processes, sample = None):  #assigns a same cluster # to records that are the same business entity
		job = utils.sample_index(self.df, sample)
		partitions_results = parallelize.parallelize(num_processes, map=self.partition, reduce=self.match).run(job)
		matches = dedupe.collect_matches(partitions_results)
		clusters = cluster.cluster(self.df, cluster='cluster', to='to', match='match').run(matches)
		return clusters
	def collect_matches(results):
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
		matches = list(np.concatenate(list(filter(lambda x: x, list(map(get_matches, results))))))  # note: empty list gets evaludated to false
		print('Worker processes terminated: Matches = ' + str(len(matches)))
		return matches
