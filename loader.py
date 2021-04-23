import pandas as pd
import geopandas
import os
import utils
import re

class loader:
	def __init__(self, entity_name, platform, entity_id, sample = None):
		self.entity_name = entity_name
		self.platform = platform
		self.entity_id = entity_id
		self.sample = sample
	# sep = chr(1)
	def run(self, path, file, sep):  #assigns a same cluster # to records that are the same business entity
		self.df = pd.read_csv(os.path.join(path, file), sep = sep)
		df = self.df
		df.rename(columns={self.entity_name: 'entity_name'}, inplace=True)
		df.rename(columns={self.platform: 'platform'}, inplace=True)
		df.rename(columns={self.entity_id: 'entity_id'}, inplace=True)
		self.__clean_and_remove_inactive()
		self.__clean_longitude_latitude()
		df.reset_index(drop=True, inplace=True)  #so index has now holes
		self.__simple_standardization_ofnames()
		print('Simple standardization: df.shape = ' + str(self.df.shape) +  ': reduced from ' + str(len(self.df.entity_name.unique())) + ' to ' + str(len(self.df.standardized_name.unique())) + ' unique names')
		df = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.longitude, df.latitude))
		if (self.sample != None):
			df = df.sample(self.sample)
		return df

	def __clean_and_remove_inactive(self):
		df = self.df
		boolMap = {True : True, False : False, 'TRUE': True, 'True': True, 'FALSE': False, 'False': False}
		print('Dropping ' + str(len(df[df['active'].isin(boolMap.keys()) == False])) + ' records due to bad active status')
		df.drop(df[df.active.isin(boolMap.keys()) == False].index, inplace = True)
		df.active = df.active.map(boolMap)
		df.drop(df[df.active == False].index, inplace = True)
	def __clean_longitude_latitude(self):
		df = self.df
		df.longitude = pd.to_numeric(df.longitude, errors='coerce')
		df.latitude = pd.to_numeric(df.latitude, errors='coerce')
		outofrange = -1000
		df.longitude = df.longitude.fillna(outofrange)
		df.latitude = df.latitude.fillna(outofrange)
		to_drop_because_latitude_outofrange = df[utils.is_outofrange(-90, 90, df.latitude)]
		to_drop_because_longitude_outofrange = df[utils.is_outofrange(-180, 180, df.longitude)]
		print('Dropping ' + str(len(to_drop_because_latitude_outofrange) + len(to_drop_because_longitude_outofrange)) + ' longitude/latitude out of range')
		df.drop(df[utils.is_outofrange(-90, 90, df.latitude)].index, inplace = True)
		df.drop(df[utils.is_outofrange(-180, 180, df.longitude)].index, inplace = True)
	def __simple_standardization_ofnames(self):
		df = self.df
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

		df.standardized_name = df.entity_name.apply(lambda x: clean_name(x))
		print('Simple standardization reduced from ' + str(len(df.entity_name.unique())) + ' to ' + str(len(df.standardized_name.unique())) + ' unique names')
