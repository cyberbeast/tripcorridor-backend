import json
from validating import Validator

class Generator:
	"""	
		Generates Cypher Query from the generator_object
		returned by the Validator()

		assumed schema for the database

		+----------------+------------+---------------+
		|  Hotel         |    Type    |   Constraint  |
		+----------------+------------+---------------+
		| name           | string     | NOT NULL      | 
		| address        | string     | NOT NULL      |
		| star_rating    | int        | (1,7)         |
		| latitude       | float      | (0.0,360.0)   |
		| longitude      | float      | (0.0,360.0)   |
		| cost_per_night | int        | INR only      |
		| adults_max     | int        | NOT zero      |
		| children_max   | int        | with adults   |
 		| check_in       | datetime   | ISO 8601      |
		| check_out      | datetime   | ISO 8601      |
		| amenities      | list of str| enumerated    |
		+----------------+------------+---------------+

		+----------------+------------+---------------+
		|  Place         |    Type    |   Constraint  |
		+----------------+------------+---------------+
		| name           | string     | NOT NULL      | 
		| address        | string     |               |
		| category       | list of str| enumerated    |
		| latitude       | float      | (0.0,360.0)   |
		| longitude      | float      | (0.0,360.0)   |
		| pricing        | int        | INR only      |
		| adults_max     | int        | NOT zero      |
		| children_max   | int        | with adults   |
		+----------------+------------+---------------+
		|                                             |
		| and other stuff you want to store like info |
		|  best season, opening hours etc.            |
		+----------------+------------+---------------+

		+----------------+------------+---------------+
		|  Destination   |    Type    |   Constraint  |
		+----------------+------------+---------------+
		| name                                        |
		|                                             |
		| and other stuff                             |
		|                                             |                
		|                                             |
		+----------------+------------+---------------+
	"""
	def _generate_hotel_query(self, data):
		"""
		generator_json = {
			"match":"hotel",
			"place":None,
			"limit":None,
			
			"class_star_rating":None,
			"distance":None,
			"distance_unit":"km",
			"budget":{"min":None,"max":None},
			"currency":"INR",
			"num_adults":2,
			"num_children":0,
			"num_nights":1,
			"check_in":None,
			"check_out":None,
			"amenities":None,
		}

		MATCH (h:Hotel) WHERE h.id = 1 RETURN h

		name	Dasharath
		type	hotel
		address	Mysore, Karnataka, India
		latitude	12.2958104
		longitude	76.6393805
		id	1
		pricing_child_cost_per_night	10070
		pricing_adult_cost_per_night	10070
		pricing_child_min	3
		pricing_adult_min	3
		rating	51
		pricing_child_max	8
		pricing_adult_max	4

		Below is a formula to calculate geodesic distance in neo4j.
		It uses haversin method. 
		CREATE (ber:City { lat: 52.5, lon: 13.4 }),(sm:City { lat: 37.5, lon: -122.3 })
		RETURN 2 * 6371 * asin(sqrt(haversin(radians(sm.lat - ber.lat))+ cos(radians(sm.lat))*
  		cos(radians(ber.lat))* haversin(radians(sm.lon - ber.lon)))) AS dist
		"""

		query = ["MATCH (p:Place), (h:Hotel)"]
		query.append("WHERE h.address =~ \".*%s.*\"" % data["place"])
		
		if data["class_star_rating"]:
			query.append("AND h.star_rating = %d" % \
				data["class_star_rating"])

		currency = 1
		if data["currency"] == "USD":
			currency = 65 # FIX ME , 1USD ~= 65INR at the time
						  # writing this line of code
						  # should also support other ISO 4217 codes
		
		if data["budget"]["min"]:
			minie = data["budget"]["min"] * currency
			query.append("AND h.cost_per_night >= %d" % minie)

		if data["budget"]["max"]:
			maxie = data["budget"]["max"] * currency
			query.append("AND h.cost_per_night <= %d" % maxie)

		if data["num_adults"]:
			query.append("AND h.adults_max >= %d" % \
				data["num_adults"])

		if data["num_children"] != 0:
			query.append("AND h.children_max >=%d" % \
				data["num_children"])

		if data["amenities"]:
			for amenity in amenities:
				query.append("AND \"%s\" IN h.amenities" % amenity)

		# FIX ME: currently check_in and check_out are ignored
		# negotiate a way to represent data and time
		# I suggest ISO 8601 format

		query.append("AND p.name = \"%s\" " % data["place"])		
		
		distance_factor = 1.0
		if data["distance_unit"] == "mile":
			distance_factor = 1.609344
		

		if data["distance"]:
			distance_condition = """AND 2 * 6371 * asin(sqrt(haversin(radians(h.latitude - p.latitude)) + cos(radians(h.latitude))*cos(radians(p.latitude))* haversin(radians(h.longitude - p.longitude)))) <= %d """ % \
				int(data['distance'] * distance_factor)
			query.append(distance_condition)
		query.append("RETURN h")	
		query.append("LIMIT %d" % data["limit"])
		return '\n'.join(query)

	def _generate_place_query(self, data):
		"""
		generator_json = {
			"match":"place",
			"destination":None,
			"limit":None,
			
			"category":None,
			"distance":None,
			"distance_unit":"km",
			"budget":{"min":None,"max":None},
			"currency":"INR",
			"num_adults":2,
			"num_children":0,
			"date":None
		}

		name	Cubbon Park
		text	Cubbon Park is a landmark 'lung' area of the Bangalore city, located within the heart of city in the Central Administrative Area.
		address	Kasturba Road, Sampangi Rama Nagar, Bangalore, Karnataka 560001
		area	120 ha
		latitude	12.9719537
		longitude	77.5936705
		id	55
		best_season_to	july
		best_season_from	august
		timings_from	8
		pricing_adult	500
		timings_to	13
		pricing_child	325


		"""
		query = ["MATCH (d)-[r:HAS]->(p:PointOfInterest)"]
		query.append("WHERE d.name =~ \".*%s.*\"" % data["destination"])
		
		if data["category"]:
			query.append("AND \"%s\" in r.categories " % \
				data["category"])


		currency = 1
		if data["currency"] == "USD":
			currency = 65 # FIX ME , 1USD ~= 65INR at the time
						  # writing this line of code
						  # should also support other ISO 4217 codes
		
		if data["budget"]["min"]:
			minie = data["budget"]["min"] * currency
			query.append("AND p.pricing >= %d" % minie)

		if data["budget"]["max"]:
			maxie = data["budget"]["max"] * currency
			query.append("AND p.pricing <= %d" % maxie)

		if data["num_adults"]:
			query.append("AND h.adults_max >= %d" % \
				data["num_adults"])

		if data["num_children"] != 0:
			query.append("AND h.children_max >=%d" % \
				data["num_children"])		
		
		distance_factor = 1.0
		if data["distance_unit"] == "mile":
			distance_factor = 1.609344
		

		if data["distance"]:
			distance_condition = """AND 2 * 6371 * asin(sqrt(haversin(radians(p.latitude - d.latitude)) + cos(radians(p.latitude))*cos(radians(d.latitude))* haversin(radians(p.longitude - d.longitude)))) <= %d """ % \
				int(data['distance'] * distance_factor)
			query.append(distance_condition)
		query.append("RETURN d,p")	
		query.append("LIMIT %d" % data["limit"])
		return '\n'.join(query)

	def generate(self, data):
		"""
			Select Query Template:

			MATCH <nodes>
			WHERE <condition>
			AND <condition> AND ...
			RETURN <nodes>
			LIMIT <int>

		"""
		query = None
		if data['match'] == 'hotel':
			query = self._generate_hotel_query(data)
		elif data['match'] == 'place':
			query = self._generate_place_query(data)
		return query

if __name__ == '__main__':

	validator = Validator()
	request_json_to_api = {
		"intent":"find hotels in a place",
		"query": "... just ignored ...",
		"entities": [
			{"value":"Bangalore","type":"place"},
			{"value":10,"type":"limit"},
			{"value":5,"type":"class_star_rating"},
			{"value":100,"type":"distance"},
			{"value":{"max":100},"type":"budget"},
			{"value":"USD","type":"currency"},
			{"value":"mile","type":"distance_unit"},
			{"value":4, "type":"num_adults"},
		],
		"others": {"ignored":"ignored"}
	}
	request2 = {
		"intent":"find places in a destination",
		"query": "... just ignored ...",
		"entities": [
			{"value":"Karnataka","type":"destination"},
			{"value":10,"type":"limit"},
			{"value":"Architecture","type":"category"},
			{"value":100,"type":"distance"},
			{"value":{"max":100},"type":"budget"},
			{"value":"USD","type":"currency"},
			{"value":"mile","type":"distance_unit"},
			{"value":4, "type":"num_adults"},
		],
		"others": {"ignored":"ignored"}
	}
# "class_star_rating":None,
# 			"distance":None,
# 			"distance_unit":"km",
# 			"budget":{"min":None,"max":None},
# 			"currency":"INR",
# 			"num_adults":2,
# 			"num_children":0,
# 			"num_nights":1,
# 			"check_in":None,
# 			"check_out":None,
# 			"amenities":None,
	okay, generator_json = validator.validate(request2)
	print "generator_json: "
	print json.dumps(generator_json, indent = 4)
	if okay and generator_json["generator_json"]["match"] in ["hotel","place"]:
		generator = Generator()
		print "Generated query is ..."
		print generator.generate(generator_json["generator_json"])
	else:
		print "error: ", json.dumps(generator_json, indent = 4)

