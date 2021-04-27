import numpy as np
import pandas as pd
import statistics
import utils
# assigns cluster to groups that all match.  The cluster column is used as cluster id, and then a 'cluster' column is added to data dataframe
class cluster:
	def __init__(self, data, cluster, to, match):
		self.df, self.cluster, self.to, self.match = data, cluster, to, match
	def run(self, matches):  #assigns a same cluster # to records that are the same business entity
		df, cluster, to, match = self.df, self.cluster, self.to, self.match
		df[cluster] = df.index  # by default each record belongs to its own cluster
		df[match] = 1.0			# each record matches with itself with 100% probability.  If a record is a member of a cluster then it will be assigned average value for its cluster
		if (len(matches) > 0):
			print('Assign clusters from matches')
			print(matches)
			matches_df = pd.DataFrame(data = matches, columns = [cluster, to, match])  			# since the match pairs are order (lowest number first) we can use the 'left' side as a cluster id
			utils.order_columns_ascending(matches_df, cluster, to)
			matches_df = matches_df.reset_index().sort_values(by=[to, cluster]).set_index(to)   	# we want to ['to', 'cluster'] but duplicates checked on 'to' only.   Then next line makes sure only first is kept
			matches_df = matches_df[~matches_df.index.duplicated()]   									# given [1 -> 2 ] and [3 -> 2 ] there should exists a [1 -> 3] as well.  So if we remove all duplicates (keeping the first - sorted by smallest) this should give us what we want
			# Note: while dropping the duplicate of [1 -> 7], and [3 -> 7] becoming [1 -> 7] would seem like a problem, because matching is symetric, there must also be a [3 -> 1] (which becomes [1 -> 3] (via order_pair) and so 3 joins the cluster
			matches_df = matches_df.reset_index()
			# assign cluster id to each cluster
			matches_df = matches_df.set_index(to)
			df.update(matches_df[cluster])
			clusterMatch = matches_df.groupby(cluster).apply(lambda group: statistics.mean(group[match])).reset_index()
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
		print('Final # record = ' + str(df.shape[0]) + ', Unique clusters = ' + str(len(df['cluster'].unique())))
		return df
