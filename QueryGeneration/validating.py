import json

class Validator:
	"""
		Validates an API request.

		self.validate(request_json_to_api)
			returns true, generator_json on success
				or
			returns false, response_json_for_more_parameters

		status can be:
			1. "missing"
			2. "success"
			3. "unknown intent"
		

		response_json_for_more_parameters has following 
		format when status has "missing"
			{
				"request_json_to_api":<input_obj_to_validator>,
				"status":"missing",

				"compulsory":{
					"found":<list of compulsory entities found>,
					"missing":<list of compulsory entities missing>
				},

				"optional":{
					"found":<list of optional entities found>,
					"missing":<list of optional entities missing>
				}
			}

		format when status has "unknown intent"
			{
				"request_json_to_api":<input_obj_to_validator>,
				"status":"unknown intent",
			}

		format when status has "success"
			{
				"request_json_to_api":<input_obj_to_validator>,
				"status":"success",
				"generator_json": <object to be passed to Generator()>
			}

		NOTE: 
			1. When status is "success", the generator_json
		is created which is to be processed by the Generator()
		object and generate the neo4j query. Then the DB is queried
		its results formatted and returned to calling API.
			2. The Validator() does not perform NLP on the query.
		For now it has been ignored in the implementation here.
		Left for the future improvements.
		


		See API-documentation.txt for details of 
		request_json_to_api
	"""

	def _check_hotel_entities(self, entities):
		"""
for "find hotels in a place" intent,
	complusory entities are:

	1. "place", around which the hotels are to be found
	2. "limit", the max number of hotel-results expected

	optional entities are:

	1. "class_star_rating", a number that in range(1,7) where
		5 for example means that the hotel is ***** (5-star) hotel
	2. "distance", the geodesic radius around the 
		place which has to be considered
	3. "distance_unit", either "km" or "mile"
	4. "budget", used to filter the hotel
		in the budget range. It is a json object
		of type {"min":<int>, "max":<int>},
		"min" is the minimum of the 
		budget range and "max" is max.
	5. "currency", ISO-4217 compliant currency code
	6. "num_adults", number of adult traveller/tourist
		default is 2
	7. "num_children", number of children, default is 0(zero)
	8. "num_nights", the number of nights for which the hotel 
		is to be checked in
	9. "check_in", date for check in
	10. "check_out", date for check out
	11. "amenities", wit.ai must return one, because we have 
		trained it exhaustively to find amenities
		Example: AC, Internet, Swimming pool, etc
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

		compulsory = {}
		compulsory["found"] = []
		compulsory["missing"] = ["place","limit"]

		optional = {}
		optional["found"] = []
		optional["missing"] = ["class_star_rating",
			"distance","distance_unit","budget","currency",
			"num_adults","num_children","num_nights","check_in",
			"check_out","amenities"]

		for entity in entities:
			
			if entity["type"] == "place":
				generator_json["place"] = entity["value"]
				compulsory["missing"].remove("place")
				compulsory["found"].append("place")

			elif entity["type"] == "limit":
				try:
					generator_json["limit"] = int(entity["value"])
					compulsory["missing"].remove("limit")
					compulsory["found"].append("limit")
				except Exception, e:
					pass
	
			elif entity["type"] == "class_star_rating":
				try:
					class_star_rating = int(entity["value"])

					if class_star_rating >= 1 and class_star_rating <= 7:
						generator_json["class_star_rating"] = class_star_rating
						optional["missing"].remove("class_star_rating")
						optional["found"].append("class_star_rating")
				except Exception, e:
					pass

			elif entity["type"] == "distance":
				try:
					distance = int(entity["value"])
					generator_json["distance"] = distance
					optional["missing"].remove("distance")
					optional["found"].append("distance")
				except Exception, e:
					pass

			elif (entity["type"] == "distance_unit" and 
				entity["value"] in ["km","mile"]):
				generator_json["distance_unit"] = entity["value"]
				optional["missing"].remove("distance_unit")
				optional["found"].append("distance_unit")

			elif entity["type"] == "budget":
				
				try:
					minie = int(entity["value"]["min"])
					generator_json["budget"]["min"] = minie
					optional["missing"].remove("budget")
					optional["found"].append("budget")
				except Exception, e:
					pass

				try:
					maxie = int(entity["value"]["max"])
					generator_json["budget"]["max"] = maxie
					optional["missing"].remove("budget")
					optional["found"].append("budget")
				except Exception, e:
					pass

			elif (entity["type"] == "currency" and 
				entity["value"] in ["INR","USD"]):
				generator_json["currency"] = entity["value"]
				optional["missing"].remove("currency")
				optional["found"].append("currency")

			elif entity["type"] == "num_adults":
				try:
					num_adults = int(entity["value"])
					generator_json["num_adults"] = entity["value"]
					compulsory["missing"].remove("num_adults")
					compulsory["found"].append("num_adults")
				except Exception, e:
					pass

			elif entity["type"] == "num_children":
				try:
					num_children = int(entity["value"])
					generator_json["num_children"] = entity["value"]
					compulsory["missing"].remove("num_children")
					compulsory["found"].append("num_children")
				except Exception, e:
					pass

			elif entity["type"] == "num_nights":
				try:
					num_nights = int(entity["value"])
					generator_json["num_nights"] = entity["value"]
					compulsory["missing"].remove("num_nights")
					compulsory["found"].append("num_nights")
				except Exception, e:
					pass

			elif entity["type"] == "check_in":
				generator_json["check_in"] = entity["value"]
				compulsory["missing"].remove("check_in")
				compulsory["found"].append("check_in")

			elif entity["type"] == "check_out":
				generator_json["check_out"] = entity["value"]
				compulsory["missing"].remove("check_out")
				compulsory["found"].append("check_out")

			elif entity["type"] == "amenities":
				generator_json["amenities"] = entity["value"]
				compulsory["missing"].remove("amenities")
				compulsory["found"].append("amenities")
		
		if len(compulsory["missing"]) != 0:
			print "Missing: ", compulsory["missing"]
			response = {
				"status": "missing",
				"compulsory": compulsory,
				"optional": optional
			}
			return False, response
		else:
			response = {
				"status":"success",
				"generator_json": generator_json,
			}
			return True, response

	def _check_place_entities(self, entities):
		"""
		for "find places in a destination" intent,
	complusory entities are:

	1."destination", a single destination or a 
		region such as "North India","Western Coast", etc,
		or a state in India suchs as"Kashmir" haha, or a
		country (you know what in mean, need example?!)
	2."limit", the max number of results expected

	optional entities are:
	1. "category", it can be one of 

	["Abseiling", "Adventure", 
	"All Destinations", "Architecture", 
	"Backpacking", "Beach", "Bird-of-paradise", 
	"Bouldering", "Buddhism","Camping", 
	"Caves", "Churches", "Climbing", 
	"College", "Crocodiles", "Culture", 
	"Cycling", "Deer", "Desert", 
	"Devaraja Market", "Elephants", "Forests", 
	"Golf", "Hill Station", "Hindu Temples", 
	"History", "Horticulture", "King Cobra", 
	"Lakes", "Mining", "Monastery", "Monument",
	"Nature", "Outdoor Recreation", "Palace", 
	"Palaces", "Paragliding", "Parasailing", 
	"Rafting", "Rainforests", "Religion", 
	"River", "Rock Climbing", "Ruins", "Safari", 
	"Safari Lodge","Scuba Diving","Sculpture",
	"Seaside Resorts","Shopping", "Snorkeling", 
	"Sports", "Surface Water Sports", "Surfing", 
	"Tech Capital With Modern-art Museums",
	"Temple", "Tigers", "Water Parks", 
	"Waterfalls", "Wildlife", "Wildlife Refuge",
	"Yoga"]

		and other values too. no default value is used

	2. "distance", the geodesic radius around the 
		destination which has to be considered
	3. "distance_unit", either "km" or "mile"
	4. "budget", used to filter the places
		in the budget range. It is a json object
		of type {"min":<int>, "max":<int>}, honestly 
		who uses <float> for currency, who cares about
		paises and cents."min" is the minimum of the 
		budget range and "max" is max.
	5. "currency", ISO-4217 compliant currency code
	6. "date", preffered day/month/year of the visit.
		used to filter places according the best season to
		visit.
	7. "num_adults", number of adult traveller/tourist
		default is 2
	8. "num_children", number of children, default is 0(zero)

		note: "num_adults" and "num_children" maybe required for 
		to filter places that have adults only constraint.
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

		compulsory = {}
		compulsory["found"] = []
		compulsory["missing"] = ["destination","limit"]

		optional = {}
		optional["found"] = []
		optional["missing"] = ["category",
			"distance","distance_unit","budget","currency",
			"num_adults","num_children","date"]

		for entity in entities:
			
			if entity["type"] == "destination":
				generator_json["destination"] = entity["value"]
				compulsory["missing"].remove("destination")
				compulsory["found"].append("destination")

			elif entity["type"] == "limit":
				try:
					generator_json["limit"] = int(entity["value"])
					compulsory["missing"].remove("limit")
					compulsory["found"].append("limit")
				except Exception, e:
					pass
	
			elif entity["type"] == "category":
				generator_json["category"] = entity["value"]
				optional["missing"].remove("category")
				optional["found"].append("category")

			elif entity["type"] == "distance":
				try:
					distance = int(entity["value"])
					generator_json["distance"] = distance
					optional["missing"].remove("distance")
					optional["found"].append("distance")
				except Exception, e:
					pass

			elif (entity["type"] == "distance_unit" and 
				entity["value"] in ["km","mile"]):
				generator_json["distance_unit"] = entity["value"]
				optional["missing"].remove("distance_unit")
				optional["found"].append("distance_unit")

			elif entity["type"] == "budget":
				
				try:
					minie = int(entity["value"]["min"])
					generator_json["budget"]["min"] = minie
					optional["missing"].remove("budget")
					optional["found"].append("budget")
				except Exception, e:
					pass

				try:
					maxie = int(entity["value"]["max"])
					generator_json["budget"]["max"] = maxie
					optional["missing"].remove("budget")
					optional["found"].append("budget")
				except Exception, e:
					pass

			elif (entity["type"] == "currency" and 
				entity["value"] in ["INR","USD"]):
				generator_json["currency"] = entity["value"]
				optional["missing"].remove("currency")
				optional["found"].append("currency")

			elif entity["type"] == "num_adults":
				try:
					num_adults = int(entity["value"])
					generator_json["num_adults"] = entity["value"]
					compulsory["missing"].remove("num_adults")
					compulsory["found"].append("num_adults")
				except Exception, e:
					pass

			elif entity["type"] == "num_children":
				try:
					num_children = int(entity["value"])
					generator_json["num_children"] = entity["value"]
					compulsory["missing"].remove("num_children")
					compulsory["found"].append("num_children")
				except Exception, e:
					pass

			elif entity["type"] == "date":
				generator_json["date"] = entity["value"]
				compulsory["missing"].remove("date")
				compulsory["found"].append("date")
		
		if len(compulsory["missing"]) != 0:
			print "Missing: ", compulsory["missing"]
			response = {
				"status": "missing",
				"compulsory": compulsory,
				"optional": optional
			}
			return False, response
		else:
			response = {
				"status":"success",
				"generator_json": generator_json,
			}
			return True, response

	def _check_trip_entities(self, entities):
		"""
		for "plan a trip" intent, 
	complusory entities are:
	
	1. "destinations", a list of destinations and 
		regions that user wants to visit
	2. "num_days", then number of days of the trip
	3. "start_date", then date from when the trip
		has to be planned

	optional entities are:
	1. "budget", the limit on the budget,
		default is unbound (infinity)
	2. "budget_class", it can be "cheapest","economy",
		"premium", or "luxury". specified when exact budget
		is not known
	2. "currency", stand currency code ISO-4217 such as 
		"INR" for indian rupees, "USD" for american
		dollar. default value is "INR" if not specified
	3. "activity_level", it can be "relaxed","normal","active"
	4. "num_adults", number of adult traveller/tourist
		default is 2
	5. "num_children", number of children, default is 0(zero)
		"""
		generator_json = {
			"match":"plan",
			"destinations":None,
			"num_days":None,
			"start_date":None,
		
			"budget":{"min":None,"max":None},
			"budget_class":None,
			"currency":"INR",
			"activity_level":None,
			"num_adults":2,
			"num_children":0
		}

		compulsory = {}
		compulsory["found"] = []
		compulsory["missing"] = ["destinations","num_days","start_date"]

		optional = {}
		optional["found"] = []
		optional["missing"] = ["budget","budget_class","currency",
			"activity_level","num_adults","num_children"]

		for entity in entities:
			
			if entity["type"] == "destinations":
				generator_json["destinations"] = entity["value"]
				compulsory["missing"].remove("destinations")
				compulsory["found"].append("destinations")

			elif entity["type"] == "num_days":
				try:
					generator_json["num_days"] = int(entity["value"])
					compulsory["missing"].remove("num_days")
					compulsory["found"].append("num_days")
				except Exception, e:
					pass
	
			elif entity["type"] == "start_date":
				generator_json["start_date"] = entity["value"]
				compulsory["missing"].remove("start_date")
				compulsory["found"].append("start_date")

			elif entity["type"] == "budget":
				
				try:
					minie = int(entity["value"]["min"])
					generator_json["budget"]["min"] = minie
					optional["missing"].remove("budget")
					optional["found"].append("budget")
				except Exception, e:
					pass

				try:
					maxie = int(entity["value"]["max"])
					generator_json["budget"]["max"] = maxie
					optional["missing"].remove("budget")
					optional["found"].append("budget")
				except Exception, e:
					pass

			elif (entity["type"] == "currency" and 
				entity["value"] in ["INR","USD"]):
				generator_json["currency"] = entity["value"]
				optional["missing"].remove("currency")
				optional["found"].append("currency")
			
			elif (entity["type"] == "budget_class" and 
				entity["value"] in ["cheapest","economy","premium","luxury"]):
				generator_json["budget_class"] = entity["value"]
				optional["missing"].remove("budget_class")
				optional["found"].append("budget_class")

			elif (entity["type"] == "activity_level" and 
				entity["value"] in ["relaxed","normal","active"]):
				generator_json["activity_level"] = entity["value"]
				optional["missing"].remove("activity_level")
				optional["found"].append("activity_level")

			elif entity["type"] == "num_adults":
				try:
					num_adults = int(entity["value"])
					generator_json["num_adults"] = entity["value"]
					compulsory["missing"].remove("num_adults")
					compulsory["found"].append("num_adults")
				except Exception, e:
					pass

			elif entity["type"] == "num_children":
				try:
					num_children = int(entity["value"])
					generator_json["num_children"] = entity["value"]
					compulsory["missing"].remove("num_children")
					compulsory["found"].append("num_children")
				except Exception, e:
					pass
		
		if len(compulsory["missing"]) != 0:
			print "Missing: ", compulsory["missing"]
			response = {
				"status": "missing",
				"compulsory": compulsory,
				"optional": optional
			}
			return False, response
		else:
			response = {
				"status":"success",
				"generator_json": generator_json,
			}
			return True, response

	def validate(self, request_json_to_api):
		intent = request_json_to_api['intent']
		entities = request_json_to_api['entities']

		if intent == "find hotels in a place":
			okay, response = self._check_hotel_entities(entities)
		elif intent == "find places in a destination":
			okay, response = self._check_place_entities(entities)
		elif intent == "plan a trip":
			okay, response = self._check_trip_entities(entities)
		else:
			okay = False 
			response = {"status": "unknown intent"}
		
		response["request_json_to_api"] = request_json_to_api
		return okay, response


if __name__ == '__main__':
	validator = Validator()
	request_json_to_api = {
		"intent":"plan a trip",
		"query": "... just ignored ...",
		"entities": [
			{"value":["Bangalore","Mysore"],"type":"destinations"},
			{"value": 3, "type": "num_days"},
			{"value": "july 1 2016", "type":"start_date"},
			{"value":10,"type":"limit"},
			{"value":"a100","type":"distance"},
			{"value":{"max":10000},"type":"budget"},
		],
		"others": {"ignored":"ignored"}
	}
	print json.dumps(validator.validate(request_json_to_api),
	 indent = 4)