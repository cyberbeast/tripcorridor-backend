"""
	A new model of workflow, where entities and intent
	is obtained from Wit.ai and only validation and 
	query/itinerary generation is done here.
"""
from validating import Validator
from generating2 import Generator
from database import Neo4jDatabase 
import json


class Model2:
	"""

		self.execute(request_json_to_api)
	"""

	def __init__(self, verbose = False, fake_db_access = False):
		self.fake_db_access = fake_db_access # if True, then truely access the Neo4jDB
		self.verbose = verbose
		self.validator = Validator()
		self.generator = Generator()
		self.neo4jdb = Neo4jDatabase()

	def _execute_cypher_query_directly(self,query):
		"""
			This method delegates the query to Neo4jDatabase
			object
		"""
		return self.neo4jdb.execute(query)

	def execute(self,request_json_to_api):
		
		print "request: ",request_json_to_api
		okay , response = self.validator.validate(request_json_to_api)
		print "response: ",json.dumps(response, indent = 4)

		if okay and response["generator_json"]["match"] in ["hotel","place"]:
			query = self.generator.generate(response["generator_json"])
			print "query: ", query
			if not self.fake_db_access:
				results = self._execute_cypher_query_directly(query)
				print "results: "
				print json.dumps(results, indent = 4)
			else:
				print "executed the above query against neo4jdb" 
			response["results"] = "Results of DB querying here"
			return response

		elif okay: #must be a "plan a trip query" for condition to be True
			print "planing a trip with following details"
			print json.dumps(response["generator_json"], indent = 4)
			response["plan"] = "Generated Itinerary here"
			return response

		else:
			print "[ERROR]: some parameters missing"
			return response

if __name__ == '__main__':
	model = Model2(verbose = True, fake_db_access = True)
	# fake_db_access is to fake DB access


	# a hotel type request
	request1 = {
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
			{"value":4, "type":"num_adults"}
		],
		"others": {"ignored":"ignored"}
	}

	# a place type request
	request2 = {
		"intent":"find places in a destination",
		"query": "... just ignored ...",
		"entities": [
			{"value":"Karnataka","type":"destination"},
			{"value":10,"type":"limit"},
			#{"value":"Architecture","type":"category"},
			{"value":100,"type":"distance"},
			{"value":{"max":100},"type":"budget"},
			{"value":"USD","type":"currency"},
			{"value":"mile","type":"distance_unit"},
			{"value":4, "type":"num_adults"}
		],
		"others": {"ignored":"ignored"}
	}	

	# a plan type request
	request3 = {
		"intent":"plan a trip",
		"query": "... just ignored ...",
		"entities": [
			{"value":["Bangalore","Goa"],"type":"destinations"},
			{"value":3,"type":"num_days"},
			{"value":"july 4 2016","type":"start_date"},

			{"value":{"max":250},"type":"budget"},
			{"value":"USD","type":"currency"},
			{"value":"mile","type":"distance_unit"},
			{"value":"relaxed","type":"activity_level"},
			{"value": 2, "type":"num_adults"}
		],
		"others": {"ignored":"ignored"}
	}

	# an error request, missing parameters
	request4 = {
		"intent":"find hotels in a place",
		"query": "... just ignored ...",
		"entities": [
	#		{"value":"Bangalore","type":"place"},
			{"value":10,"type":"limit"},
			{"value":5,"type":"class_star_rating"},
			{"value":100,"type":"distance"},
			{"value":{"max":100},"type":"budget"},
			{"value":"USD","type":"currency"},
			{"value":"mile","type":"distance_unit"},
			{"value":4, "type":"num_adults"}
		],
		"others": {"ignored":"ignored"}
	}

	model.execute(request3)
		
