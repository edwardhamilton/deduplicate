import numpy as np
import pandas as pd
import statistics
import networkx as nx
from functools import reduce
import utils
# assigns cluster to groups that all match.  The cluster column is used as cluster id, and then a 'cluster' column is added to data dataframe
class cluster:
	def __init__(self, data, cluster, to, match):
		self.df, self.cluster, self.to, self.match = data, cluster, to, match
	def run(self, matches):  #assigns a same cluster # to records that are the same business entity
		df, cluster, to, match = self.df, self.cluster, self.to, self.match
		df['cluster'] = df.index  # by default each record belongs to its own cluster
		df[match] = 1.0			# each record matches with itself with 100% probability.  If a record is a member of a cluster then it will be assigned average value for its cluster

		if (len(matches) > 0):
			print('Assign clusters from ' + str(len(matches)) + ' matches')
			G = nx.Graph()
			G.add_weighted_edges_from(list(map(tuple, matches)))
			def get_avg_weight(vertex):
				edges = list(vertex.values())
				return reduce(lambda a, b: { 'weight': a['weight'] + b['weight'] }, edges)['weight'] / len(edges)
			starting_clusterid = df.shape[0]
			data = [[starting_clusterid + i, element, get_avg_weight(G[element])] for i, component in enumerate(nx.connected_components(G), 1) for element in component]
			cluster_df = pd.DataFrame(data=data, columns=['cluster', 'index', match])
			avg_match = statistics.mean(cluster_df[match])
			min_match = min(cluster_df[match])
			max_match = max(cluster_df[match])
			cluster_df = cluster_df.set_index('index')
			df.update(cluster_df['cluster'])
			clusterMatch = cluster_df.groupby(cluster).apply(lambda group: statistics.mean(group[match])).reset_index()
			clusterMatch.columns = [cluster, match]
			df.set_index(cluster, inplace=True)
			df.update(clusterMatch.set_index(cluster))
			df.reset_index(inplace=True)
			df['cluster_temp'] = df[cluster]
			cluster_size_df = df.cluster_temp.value_counts().rename_axis('cluster_temp').reset_index(name='cluster_size')
			df = df.set_index('cluster_temp').join(cluster_size_df.set_index('cluster_temp'))
			df = df.sort_values(by=['cluster_size', cluster], ascending=False)  # its convenient to have largest clusters first when opening in excel
			df[match] = (df[match] * 100).astype(int)		# easier to filter (in excel) when % are integers
			df.rename(columns={self.cluster: 'cluster'}, inplace=True)
		print('Final # record = ' + str(df.shape[0]) + ', Unique clusters = ' + str(len(df['cluster'].unique())) + ', Match: Avg = ' + str(avg_match) + ', Min = ' + str(min_match) + ', Max = ' + str(max_match) + ', # clusters = ' + str(cluster_df.shape[0]))
		return df
