import labeled_pairs
import model
from googleplaces import GooglePlaces, types, lang
#YOUR_API_KEY = 'AIzaSyAsMgzumVHXhwbrFd-Blca292rJwuiCCwY'
class auto_labeler(pair_labeler):
	def __init__(self, YOUR_API_KEY, model):
		super().__init__(model)
		self.google_places = GooglePlaces(YOUR_API_KEY)
	def run(self, left, right):
		query_result = google_places.nearby_search(
		        lat_lng={'lat': 33.8496815, 'lng': -84.255114},
		        radius=500,
		        types=[types.TYPE_RESTAURANT] or [types.TYPE_CAFE])
		query_result.places
				self.present_pair_characteristics_to_user(left, right)
				self.get_label_from_user(row)
		# if right is best match with left from places query then its a match.  Need to work out a few details
