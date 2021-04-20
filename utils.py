
class utils:
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
		
class Range(object):
	def __init__(self, start, end):
		self.start = start
		self.end = end
	def __eq__(self, other):
		return self.start <= other <= self.end
	def __str__(self):
		return 'range(' + str(self.start) + ',' + str(self.end) + ')'		
def trace(msg):
	pass
	#print(str(_wid) + ': ' + msg)
		
