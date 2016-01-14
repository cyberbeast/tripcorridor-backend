import json

class Formatter:
	" Formatter: (noun) something that knows how to format!"
	def format(self, resultset):
		results = []

		for result in resultset:
			res = {}
			room_details = {}
			hotel_details = {}
			for key in dir(result):
				if not key.startswith('_'):
					if key in ["room_type","cost",
					"rate_time_unit","max_adults","max_children"]:
						room_details[key] = result[key]
					elif key == "dist":
						res["distance"] = result[key]
					else:
						res[key] = result[key]
			if room_details != {}:
				res["room_details"] = room_details
			res = {"hotel":res}
		
			results.append(res)

		return results
