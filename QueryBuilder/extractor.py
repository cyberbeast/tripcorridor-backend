import json

class Extractor:
	"""
		Extracts data from wit ai response and get is in the 
		following format called Intermediate Representation 1.

		IR1 = { 
			"location": <str>,
			"rating": <None|{
				"min": <int|None>,
			 	"max": <int|None>, 
			 	"exact": <int|None>
			 }>,
			"amenities": <None | list of str>,
			"roomtype": <None |roomtype dict>
			"limit" : <int>
		}
			where <roomtype dict> is 
				{
					<rtype>: <None |{
						"cost":{
							"min": <int|None>,
							"max": <int|None>,
							"exact": <int|None>,
						},
						"children": <int>,
						"adults": <int>,
			 		} >,
			 	}
			where <rtype> is one of 
				1. any - for any hotel
				2. Deluxe 
				3. Standard A/C Room
				4. Standard Non A/C Room
				5. Suite

	"""
	def extract(self,wit_ai_response):
		outcomes = wit_ai_response["outcomes"]
		outcome = outcomes[0]
		entities = outcome["entities"]

		ret = {
			"location": None,
			"amenities": None,
			"rating": None,
			"roomtype": None,
			"limit": 25
		}

		ret["location"] = self._extract_location(entities)
		ret["amenities"] = self._extract_amenities(entities)
		# ret["class_star_rating"] = self._extract_class_star_rating(entities)
		# ret["distance"] = self._extract_distance(entities)
		# ret["budget"] = self._extract_budget(entities)
		print "=" * 20 + "INTERMEDIATE REPRESENTATION" + "=" * 20
		print json.dumps(ret, indent = 4)
		return ret

	def _parse_recursively(self, json_obj, key):

		if type(json_obj) == dict:
			for k, v in json_obj.items():
				# print "k:", k
				# print "v:", v 
				if k == key:
					return v
				elif type(v) == dict:
					ret = self._parse_recursively(v,key)
					if ret:
						return ret 
				elif type(v) == list:
					for elem in v:
						ret = self._parse_recursively(elem, key)
						if ret:
							return ret
		elif type(json_obj) == list:
			for elem in json_obj:
				ret = self._parse_recursively(elem, key)
				if ret:
					return ret 

	def _extract_amenities(self, entities):
		amenities = []
		ams = self._parse_recursively(entities,"accomodation_amenity")
		if ams:
			for am in ams:
				amenities.append(str(am["value"]))
		if amenities:
			return amenities
		else:
			return None

	def _extract_class_star_rating(self,entities):
		if entities.has_key("class_star_rating"):
			return entities["class_star_rating"][0]["value"]

	def _extract_location(self,entities):
		# print "entities: ", entities
		location = self._parse_recursively(entities,"location")
		# print "location: ", location
		if location:
			splits = location[0]["value"].split()
			caps = [word.capitalize() for word in splits]
			location = " ".join(caps)
			return location
		else:
			return "India" #Hard coded value for location


	def _extract_distance(self,entities):
		if entities.has_key("distance"):
			unit = entities["distance"][0]["unit"]
			value = entities["distance"][0]["value"]
			if unit == "mile":
				value *= 1.60934
			return value

	def _extract_budget(self, entities):
		budget = {"min":None,"max":None,"avg":None}
		unit = "INR"
		if entities.has_key("amount_of_money"):
			value = entities["amount_of_money"][0]["value"]
			unit = entities["amount_of_money"][0]["unit"]
			if unit in ['$',"USD"]:
				value *= 65 #Nominal value of INR in USD
			budget["avg"] = value
		if entities.has_key("min"):
			value = entities["min"][0]["value"]
			unit = entities["min"][0]["unit"]
			if unit in ['$',"USD"]:
				value *= 65 #Nominal value of INR in USD
			budget["min"] = value
		if entities.has_key("max"):
			value = entities["max"][0]["value"]
			unit = entities["max"][0]["unit"]
			if unit in ['$',"USD"]:
				value *= 65 #Nominal value of INR in USD
			budget["max"] = value
		if entities.has_key("number"):
			number = entities["number"][0]["value"]
			if unit in ['$',"USD"]:
				number *= 65
			if budget["min"] and not budget["max"]:
				budget["max"] = number
			if budget["max"] and not budget["min"]:
				budget["min"] = number	

		if budget["min"] > budget["max"]: #then swap
			budget["min"],budget["max"] = budget["max"],budget["min"]	
		return budget

	def _extract_adult(self, entities):
		pass

	def _extract_children(self, entities):
		pass

	def _extract_duration(self, entities):
		pass

	def _extract_check_in(self, entities):
		pass

	def _extract_check_out(self, entities):
		pass
