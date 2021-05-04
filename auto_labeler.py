from googleplaces import GooglePlaces, types, lang
import labeler
import model
import utils
#YOUR_API_KEY = 'AIzaSyAsMgzumVHXhwbrFd-Blca292rJwuiCCwY'


valid_types = [types.TYPE_BAKERY,types.TYPE_BAR, types.TYPE_CAFE, types.TYPE_CONVENIENCE_STORE, types.TYPE_ESTABLISHMENT, types.TYPE_FOOD, types.TYPE_LIQUOR_STORE, types.TYPE_MEAL_TAKEAWAY, types.TYPE_RESTAURANT]
class auto_labeler(labeler.pair_labeler):
	def __init__(self, API_KEY, radius):
		super().__init__()
		self.google_places = GooglePlaces(API_KEY)
		self.raduis = radius
	def run(self, left, right, match):
		lng = utils.average(self.parent.df.iloc[left].longitude, self.parent.df.iloc[right].longitude)
		lat = utils.average(self.parent.df.iloc[left].latitude, self.parent.df.iloc[right].latitude)
		places = self.google_places.nearby_search(
		        lat_lng={'lat': lat, 'lng': lng},
		        radius=self.raduis).places
		left_best_match = best_places_match(places, self.parent.df.iloc[left].standardized_name)
		right_best_match = best_places_match(places, self.parent.df.iloc[right].standardized_name)
		print(left_best_match, right_best_match)
		if (left_best_match == right_best_match):
			return labeler.LABEL.MATCH
		else:
			return labeler.LABEL.NOTMATCH

		# if right is best match with left from places query then its a match.  Need to work out a few details
