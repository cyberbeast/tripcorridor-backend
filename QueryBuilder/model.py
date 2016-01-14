from database import Neo4jDatabase
from formatter import Formatter 
from extractor import Extractor
from builder import Builder, pp
from gobbledygook import parsed_args, IR1
import json

class Model(object):

	def __init__(self):
		self.db = Neo4jDatabase()
		self.fmtr = Formatter()
		self.bldr = Builder()
		self.xtrctr = Extractor()

	def execute(self, parsed_args):

		response = {
			"status": "success",
			"results": [],
			"count": 0
		}

		
		extract = self.xtrctr.extract(parsed_args["backend_request"])
		
		query = self.bldr.build(extract)
		
		if not query["query"]:
			print "=" * 30 + "ERROR" + "=" * 30
			print "Message: ", query["message"]
			response["status"] = "failed"
			response["message"] = query["message"]
			return response

		resultset = self.db.simply_query(query["query"])
		response["results"] = self.fmtr.format(resultset)
		response["count"] = len(response["results"])

		return response

if __name__ == '__main__':

	model = Model()
	pp(model.execute(parsed_args))