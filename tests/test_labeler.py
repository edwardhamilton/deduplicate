import numpy as np
import pandas as pd
import geopandas
import statistics
import unittest
import math
import sys
import helpers
import os
from googleplaces import GooglePlaces, types, lang
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

sys.path.append('../')
import dedupe
import utils
import partition
import match
import filter_Distance
import filter_TfidfCosSimilar_and_Distance
import model_Fuzz
import model_Xgboost
import manual_labeler
import labeler

class null_labeler(labeler.pair_labeler):
	def __init__(self):
		super().__init__(model=None)
	def run(self, left, right, match):
		return labeler.LABEL.QUIT

class Test_Labeler(unittest.TestCase):
	@utils.ignore_warnings
	def setUp(self):
		self.path = 'datasets'
		self.train_file = 'trainset.csv'
		self.df = helpers.load_dataset()
		self.filter = filter_TfidfCosSimilar_and_Distance.filter_TfidfCosSimilar_and_Distance(self.df, ngram_range=(1,4), min_name_vectorization_word_frequency=0.0,
			max_name_vectorization_word_frequency=.8, topn_by_cosine_similarity=30,
			min_cosine_similarity=.2, topn_matches_to_apply_model_to=1000, max_distance=150)
		self.model = model_Xgboost.model_Xgboost(self.df, match_probability = .5, path = self.path, train_file = self.train_file)
		self.match=match.match(self.filter, self.model)
		self.partition=partition.partition(data=self.df, divisor=4, max_span=50, max_size=2000)
		self.dedupe = dedupe.dedupe(data=self.df, partition=self.partition, match=self.match)


	@utils.ignore_warnings
	def __test_null_labeler(self):
		pair_labeler = null_labeler()
		labeler.labeler(num_processes=1, data=self.df,
			dedupe=self.dedupe,
			pair_labeler=pair_labeler, path=self.path, train_file=self.train_file, sample=100000).run()
	@utils.ignore_warnings
	def test_manual_labeler(self):
		YOUR_API_KEY = 'AIzaSyAsMgzumVHXhwbrFd-Blca292rJwuiCCwY'
		google_places = GooglePlaces(YOUR_API_KEY)
		# You may prefer to use the text_search API, instead.
		query_result = google_places.nearby_search(lat_lng={'lat': 33.8496815, 'lng': -84.255114}, radius=150)
		print(query_result.places)
		pair_labeler = manual_labeler.manual_labeler()
		labeler.labeler(num_processes=1, data=self.df,
			dedupe=self.dedupe,
			pair_labeler=pair_labeler, path=self.path, train_file=self.train_file, sample=10000).run()


if __name__ == '__main__':
    unittest.main()
