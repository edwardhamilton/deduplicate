'''
 Edward Hamilton (4/11/2021):  https://www.linkedin.com/in/edward-h-b674a76/
 
 Matching Algorithm:
 1. Clean data
 2. Train Xgboost Classifier to predict match (T/F) or bad data: Features - 3 FuzzyWuzzy ratios, distance (between matches), name length ratios, name word count ratios, whether restaurant_id matches, and whether platform matches.
 2. Partition into smaller regions
 3. Generated a set of potential matches via cosine similarity filtering
 4. Classify as (match/not-match/bad data) via Xgboost model.
 5. Assign cluster ids
 
 Building Labeled Training set:
 1. Run without prediction model, using FuzzyWuzzy.ratio instead.  Essentially this just applies the cosine similarity and distance filters, which is what the eventual model will see.  So we want to train on this
 2. Randomly select N records from this and let use choose 'Match', 'No-Match', or 'bad data'.    Since there are 8 features, there should be at least 80 rows in our training set.
	Note: every time bad data is selected, the name is added to collection of 'bad' names.  Need to think about model to use to predict bad names
 
 Workflow:
 1. Build labelled  training set
 2. Run matching algorithm
 
 QA:
 1.  I sort output dataset by 'match' probability (ascending) and visually spotcheck the records with worse match probability
 2.  If we want to check whether we're undermatching, we can reduce the 'match_probability' and see if we catching more good matches .vs bad matches.
 3.  I've added a little quality testing of the Classification Model, during manual training set labeling, if there an existing training set, it will train on that first, then during labeling it can check for false positives/negatives.
	 It also sorts the training set on worse prediction probability so that these can be labed first.   we show to see enough difficult matches for labeling
 4.  I haven't done any statistical analysis of overall deduplication error.  Just manual spot checking.
 
 Improvements:  
 1. I think the components (partitioning, filtering, classification, training set labeling tool) are there, but it needs more data science.  Haven't yet done much feature engineering or hyperparameter tuning.  The set of feature
    for classification are pretty much the first thing that came into mind.
 2. might consider vectorizing names with language models (e.g. fasttext, word-2vec).  Also we would want to 
 3. develope model to predict bad-records
 4. Auto training set labeling: We might do google map search around the business location to see if there are more than 1 entity with similar name (within a 150 meter radius), if not then its unique.
 5. predict
 
	GeoText: location mentions that are far from location may be significant

 USAGE:
	python deduplicate.py -help
	python deduplicate.py  --path "C:\\CloudKitchens" --runfile "css_public_all_ofos_locations.csv" --trainfile "output_SUPERVISED_MATCH.csv" --buildtrainset "trainset.csv"
	python deduplicate.py  --path "C:\\CloudKitchens" --runfile "css_public_all_ofos_locations.csv" --trainfile "trainset.csv" --buildtrainset "trainset.csv" --sample 1000
	python deduplicate.py  --path "C:\\CloudKitchens" --runfile "css_public_all_ofos_locations.csv" --trainfile "trainset.csv" --sample 1000

		Note: if you resort or modify the run_file, you'll need to generate a clean training set as it relies on the row indices
 BUGS:
	1.  There maybe be a bug in assigning the cluster size and/or and average cluster match probabilities.   I see a few records that have cluster size 1 with match probability < 100% (as a cluster of size one always matches with itself 100%)
	

	
'''
import pandas as pd 
import geopandas
import geotext
from geotext import GeoText
import statistics
from cartopy import crs as ccrs
from shapely.ops import nearest_points
import shapely.geometry
import numpy as np
import math
from math import radians, cos, sin, asin, sqrt
from fuzzywuzzy import fuzz
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score, KFold
import itertools
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
import sparse_dot_topn.sparse_dot_topn as ct
from sparse_dot_topn import awesome_cossim_topn
import queue

import itertools
import re
import time
import multiprocessing
import sys
import os
import argparse
import pathlib
from getch import getch, pause

# globals

def trace(msg):
	pass
	#print(str(_wid) + ': ' + msg)
	
	


################ MAIN ####################### 
main = main()
main.run()
#############################################
