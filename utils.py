from math import radians, cos, sin, asin, sqrt
import numpy as np
import pandas as pd
from random import random

#todo need to add this back in otherwise clustering will not be correct
def order_pair(left, right):  # this makes it easier to assign cluster id, as first in match pair.
	if (left <= right):
		return left, right
	return right, left

def randfloat(f, t, size):
	return f + np.random.random(size=size) * (t - f)

def order_columns_ascending(df, a, b):
	df[a], df[b] = np.where(df[a] < df[b], [df[a], df[b]], [df[b], df[a]])  # make sure smaller number is the cluster

def swap_columns_randomly(df, a, b):
	df[a], df[b] = np.where(random() > .5, [df[a], df[b]], [df[b], df[a]])   # randomly swap left and right.

def haversine(lon1, lat1, lon2, lat2):
	"""
	Calculate the great circle distance between two points
	on the earth (specified in decimal degrees)
	"""
	# convert decimal degrees to radians
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	# haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a))
	# Radius of earth in kilometers is 6371
	km = 6371* c
	return km
def is_outofrange(f, t, x):
	return (x < f) | (x > t)
def get_distance(lt, rt):
	return int(haversine(lt.longitude, lt.latitude, rt.longitude, rt.latitude) * 1000.0)

def apply(df, func, columns):
	s = df.apply(lambda x: func(x), axis=1)
	tf = pd.DataFrame.from_dict(dict(zip(s.index, s.values))).T
	tf.columns = list(columns.keys())
	df = df.merge(tf, left_index=True, right_index=True)
	return df.astype(columns)



class Range(object):
	def __init__(self, start, end):
		self.start = start
		self.end = end
	def __eq__(self, other):
		return self.start <= other <= self.end
	def __str__(self):
		return 'range(' + str(self.start) + ',' + str(self.end) + ')'
