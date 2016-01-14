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
			"distance": None,
			"limit": 25
		}

		ret["location"] = self._extract_location(entities)
		ret["amenities"] = self._extract_amenities(entities)
		ret["rating"] = self._extract_class_star_rating(entities)
		ret["distance"] = self._extract_distance(entities)
		ret["roomtype"] = self._extract_roomtype(entities)
		print "=" * 20 + "INTERMEDIATE REPRESENTATION" + "=" * 20
		print json.dumps(ret, indent = 4)
		return ret

	def _parse_recursively(self, json_obj, key):
		" Very tricky to write this function. Took me a while. "
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
		rating = self._parse_recursively(entities,"class_star_rating")
		values = []
		if rating:
			ret = { "min" : None, "max": None, "exact": None}
			for rt in rating:
				values.append(rt["value"])
			if len(values) == 1:
				ret["exact"] = values[0]
			else:
				ret["min"] = min(values)
				ret["max"] = max(values)
			return ret 

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
		distance = self._parse_recursively(entities,"distance")
		values = []
		if distance:
			unit = distance[0]["unit"]

			distance_factor = 1.0

			if unit == "mile":
				distance_factor = 1.60934
			
			ret = { "min" : None, "max": None, "exact": None}
			for dis in distance:
				values.append(dis["value"])
			
			if len(values) == 1:
				ret["exact"] = values[0] * distance_factor
			else:
				ret["min"] = min(values) * distance_factor
				ret["max"] = max(values) * distance_factor
		
			return ret

	def _extract_roomtype(self, entities):


		roomtype = self._parse_recursively(entities,"accomodation_room_type")
		cost = self._extract_cost(entities)
		duration = self._extract_duration(entities)
		adults = self._extract_num_adults(entities)
		children = self._extract_num_children(entities)

		if roomtype:
			roomtype = roomtype[0]["value"]

		if not roomtype:
			roomtype = "any"

		ret = {
			str(roomtype): {
				"cost": cost,
				"adults": adults,
				"children": children,
				"duration": duration
			}
		}

		print "RET", ret 

		if (cost["min"] or cost["max"] or cost["exact"] 
			or adults or children or (roomtype and roomtype != "any")):
			return ret

	def _extract_cost(self, entities):
		budget = {"min":None,"max":None,"exact":None}
		unit = "INR"
		USD_to_INR = 65
		amount_of_money = self._parse_recursively(entities,"amount_of_money")
		if amount_of_money:
			value = amount_of_money[0]["value"]
			unit = amount_of_money[0]["unit"]
			if unit in ['$',"USD"]:
				value *= USD_to_INR #Nominal value of INR in USD
			budget["exact"] = value

		cost_min = self._parse_recursively(entities,"min")
		if cost_min:
			value = cost_min[0]["value"]
			unit = cost_min[0]["unit"]
			if unit in ['$',"USD"]:
				value *= USD_to_INR #Nominal value of INR in USD
			budget["min"] = value

		cost_max = self._parse_recursively(entities,"max")
		if cost_max:
			value = cost_max[0]["value"]
			unit = cost_max[0]["unit"]
			if unit in ['$',"USD"]:
				value *= USD_to_INR #Nominal value of INR in USD
			budget["max"] = value

		number = self._parse_recursively(entities,"number")
		if number:
			number = number[0]["value"]
			if unit in ['$',"USD"]:
				number *= USD_to_INR
			if budget["min"] and not budget["max"]:
				budget["max"] = number
			if budget["max"] and not budget["min"]:
				budget["min"] = number	

		if budget["min"] > budget["max"]: #then swap
			budget["min"],budget["max"] = budget["max"],budget["min"]	
		
		return budget

	def _extract_num_adults(self, entities):
		adults = self._parse_recursively(entities,"adults")
		num_adult = 0
		if adults:
			for adult in adults:
				num_adult += adult["value"]
			return num_adult

	def _extract_num_children(self, entities):
		children = self._parse_recursively(entities,"children")
		num_child = 0
		if children:
			for child in children:
				num_child += child["value"]
			return num_child

	def _extract_duration(self, entities):
		duration = self._parse_recursively(entities,"duration")
		if duration:
			pass	
		return 24 # Hard coded value for duration

	def _extract_check_in(self, entities):
		pass

	def _extract_check_out(self, entities):
		pass
