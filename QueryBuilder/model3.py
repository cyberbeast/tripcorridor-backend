from database import Neo4jDatabase

class Model3(object):
	def execute(self, parsed_args):
		print 'parsed_args are:',parsed_args
		return {'parsed_args':parsed_args}


class Extractor:
	def extract(self,wit_ai_response):
		outcomes = wit_ai_response["outcomes"]
		outcome = outcomes[0]
		entities = outcome["entities"]
		ret = {}
		ret["class_star_rating"] = self._extract_class_star_rating(entities)
		ret["locations"] = self._extract_location(entities)
		ret["distance"] = self._extract_distance(entities)
		ret["budget"] = self._extract_budget(entities)
		return ret

	def _extract_class_star_rating(self,entities):
		if entities.has_key("class_star_rating"):
			return entities["class_star_rating"][0]["value"]

	def _extract_location(self,entities):
		if entities.has_key("location"):
			locs = []
			for loc in entities["location"]:
				if not loc["value"].isdigit():
					locs.append(loc["value"])
			return locs


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

class Neo4jQueryBuilder(object):
	
	def build(self, wit_ai_response):
		pass
	
	def extract(self,wit_ai_response):
		
		extractor = Extractor()
		entities = extractor.extract(wit_ai_response)
		return entities


parsed_args = { "wit_ai_response": {
			"_text": "Find 5 star hotels in Bangalore from rupees 3000 to 5000 under 200 km from july 2016", 
			"msg_id": "fbb61a61-8a8d-41cb-9b3d-961b308c12ef", 
			"outcomes": [
				{
					"_text": "Find 5 star hotels in Bangalore from rupees 3000 to 5000 under 200 km from july 2016", 
					"confidence": 0.91, 
					"entities": {
						"accomodation_qualifier": [
							{
								"type": "value", 
								"value": "find"
							}, 
							{
								"type": "value", 
								"value": "hotels"
							}
						], 
						"class_star_rating": [
							{
								"type": "value", 
								"value": 5
							}
						], 
						"datetime": [
							{
								"grain": "month", 
								"type": "value", 
								"value": "2016-07-01T00:00:00.000-07:00", 
								"values": [
									{
										"grain": "month", 
										"type": "value", 
										"value": "2016-07-01T00:00:00.000-07:00"
									}
								]
							}
						], 
						"distance": [
							{
								"type": "value", 
								"unit": "mile", 
								"value": 200
							}
						], 
						"location": [
							{
								"suggested": True, 
								"type": "value", 
								"value": "Bangalore"
							}
						], 
						"max": [
							{
								"type": "value", 
								"unit": "INR", 
								"value": 3000
							}
						], 
						"number": [
							{
								"type": "value", 
								"value": 5000
							}
						]
					}, 
					"intent": "hotel_discovery"
				}
				]
			}
			}


if __name__ == '__main__':
	nqb = Neo4jQueryBuilder()
	extract = nqb.extract(parsed_args["wit_ai_response"])
	print extract