from math import radians, cos, sin, asin, sqrt
import numpy as np
import pandas as pd
from random import random
import warnings
from fuzzywuzzy import fuzz

def sample_index(df, sample = None):
	return list(df.sample(sample).index if (sample != None) else df.index)



def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_func(self, *args, **kwargs)
    return do_test

def average(a, b):
  return (a + b) / 2.0
  
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
def best_places_match(places, value):
	comparisons = list(map(lambda x: (x.name, fuzz.ratio(x.name, value)), places))
	return reduce(lambda a, b: a if (a[1] > b[1]) else b, comparisons)


def apply(df, func, columns):
	try:
		s = df.apply(lambda x: func(x), axis=1)
		tf = pd.DataFrame.from_dict(dict(zip(s.index, s.values))).T
		tf.columns = list(columns.keys())
		df = df.merge(tf, left_index=True, right_index=True)
		return df.astype(columns)
	except Exception as e:
		print('catch7')
		print(e)
		print(df)
		return df

class Range(object):
	def __init__(self, start, end):
		self.start = start
		self.end = end
	def __eq__(self, other):
		return self.start <= other <= self.end
	def __str__(self):
		return 'range(' + str(self.start) + ',' + str(self.end) + ')'
