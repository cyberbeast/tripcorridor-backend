from database import Neo4jDatabase
from formatter import Formatter
import json

def pp(json_obj):
	print json.dumps(json_obj, indent = 4)

class Builder:
	"""Builds the Neo4j Cypher Query

	   It turns (Intermediate Represtation 1)(INPUT),

		IR1 = { 
			"location": "Bangalore Division",
			"rating": {"min": 3, "max": 5, "exact": None},
			"amenities": ["WiFi","Gym","Cafe"],
			"roomtype":{
				"any":{
					"cost":{
						"min": 1000,
						"max": 12000,
						"exact": None,
					},
					"children": 4,
					"adults": 6,
			 	},
			},
			"limit" : 25
		}

		into (Neo4j Cypher Query)(OUTPUT),

		MATCH (dv:Division)-->(d:District),
		 (d)-->(h:Hotel),
		 (h)-->(r:Rating),
		 (h)-->(a:Amenity),
		 (h)-[rd]->(rt:RoomType)
		WHERE r.scale <= 5
		 AND r.scale >= 3
		 AND a.name IN ['WiFi', 'Gym', 'Cafe']
		 AND rd.cost <= 12000
		 AND rd.cost >= 1000
		 AND rd.max_adults >= 6
		 AND rd.max_children >= 4
		RETURN REDUCE(addr = d.name , n IN [dv] |  		
		 addr + ", " + n.name) AS hotel_address,
		 h.name AS hotel_name,
		 r.scale AS class_star_rating,
		 COLLECT(a.name) AS amenities,
		 rd.max_adults AS max_adults,
		 rd.max_children AS max_children,
		 rt.type AS room_type,
		 rd.cost AS cost,
		 rd.duration AS duration
		LIMIT 25

		More documentation later...
	"""
	traversal_query = {
		"Country": "(c:Country)-->(s)-->(d:District)",
		"Region":"(rg:Region)-->(s)-->(d:District)",
		"State": "(s:State)-->(d:District)",
		"UnionTerritory": "(ut:UnionTerritory)-->(d:District)",
		"Division": "(dv:Division)-->(d:District)",
		"District": "(d:District)",
	}

	return_vars = {
		"Country":        "s,c",
		"Region":         "s,rg",
		"State":          "s",
		"UnionTerritory": "ut",
		"Division":       "dv",
		"District":       "",
	}
	loc_vars = {
		"Country":        "c",
		"Region":         "rg",
		"State":          "s",
		"UnionTerritory": "ut",
		"Division":       "dv",
		"District":       "d",
	}

	def __init__(self):
		self.db = Neo4jDatabase()

	def resolve_address(self,location):
		query = """
			MATCH (loc:Location)
			WHERE loc.name = \"{0}\"
			OR loc.headquarter = \"{0}\"
			OR loc.alternate_name = \"{0}\"
			RETURN loc.name as name,
			labels(loc) as labels 
		""".format(location)

		labels = self.db.simply_query(query)
		if labels:
			names= [label["name"] 
				for label in labels]
			labels = labels[0]["labels"]
			labels.remove("Location")
			# if len(names) == 1:
			# 	names = names[0]
			return ([str(name) for name in names], labels[0])
		else:
			return None

		return traversal_query

	def address_hierarchy_query(self, locations, label):
		query = """
			MATCH {traversal_query}
			WHERE {loc_var}.name IN {locations}
			RETURN REDUCE(addr = d.name , n IN [{return_vars}] | 
				addr + ", " + n.name) as address
			LIMIT 10
		"""



		feeds = {}
		feeds["traversal_query"] = self.traversal_query[label]
		feeds["loc_var"] = self.loc_vars[label]
		feeds["locations"] = locations
		feeds["return_vars"] = self.return_vars[label]
		return query.format(**feeds)

	def build_stage_1(self, IR1):

		IR2 = { "MATCH": [],
			"WHERE": [],
			"RETURN": [],
			"LIMIT": None
		}

		result = self.resolve_address(IR1["location"])
		if not result:
			raise Exception("Could not Resolve Address: %s" % IR1["location"])
			

		locations, label = result
		IR2["MATCH"].append(self.traversal_query[label])
		IR2["WHERE"].append("%s.name IN %s" % ((self.loc_vars[label],locations)))
		reduction = "REDUCE(addr = d.name , n IN [%s] | \
 		\n addr + \", \" + n.name) AS hotel_address"
		reduction %= self.return_vars[label]

		IR2["RETURN"].append(reduction)

		IR2["MATCH"].append("(d)-->(h:Hotel)")
		IR2["RETURN"].append("h.name AS hotel_name")

		if IR1["rating"]:
			rmin = IR1["rating"]["min"]
			rmax = IR1["rating"]["max"]
			rexact = IR1["rating"]["exact"]

			IR2["MATCH"].append("(h)-->(r:Rating)")
			if rexact:
				IR2["WHERE"].append("r.scale = %d" % rexact)
			else:
				if rmax:
					IR2["WHERE"].append("r.scale <= %d" % rmax)
				if rmin:
					IR2["WHERE"].append("r.scale >= %d" % rmin)
			IR2["RETURN"].append("r.scale AS class_star_rating")

		if IR1["amenities"]:
			amenities = IR1["amenities"]
			IR2["MATCH"].append("(h)-->(a:Amenity)")
			IR2["WHERE"].append("a.name IN %s" % str(amenities))
			IR2["RETURN"].append("COLLECT(a.name) AS amenities")

		if IR1["roomtype"]:
			IR2["MATCH"].append("(h)-[rd]->(rt:RoomType)")

			rtype = IR1["roomtype"].keys()[0]
			room_detail = IR1["roomtype"].values()[0]
			if rtype != "any":
				IR2["WHERE"].append("rt.type = \"%s\"" % rtype)

			cmax = room_detail["cost"]["max"]
			cmin = room_detail["cost"]["min"]
			cexact = room_detail["cost"]["exact"]

			if cexact:
				IR2["WHERE"].append("rd.cost = %d" % cexact)
			else:
				if cmax:
					IR2["WHERE"].append("rd.cost <= %d" % cmax)
				if cmin:
					IR2["WHERE"].append("rd.cost >= %d" % cmin) 

			if room_detail["adults"]:
				num_adults = room_detail["adults"]
				IR2["WHERE"].append("rd.max_adults >= %d" % num_adults)
				IR2["RETURN"].append("rd.max_adults AS max_adults")

			if room_detail["children"]:
				num_children = room_detail["children"]
				IR2["WHERE"].append("rd.max_children >= %d" % num_children)
				IR2["RETURN"].append("rd.max_children AS max_children")

			
			IR2["RETURN"].append("rt.type AS room_type")
			IR2["RETURN"].append("rd.cost AS cost")
			IR2["RETURN"].append("rd.duration AS rate_time_unit")
	

		if IR1["limit"]:
			IR2["LIMIT"] = IR1["limit"]

		return IR2

	def build_stage_2(self, IR2):
		IR3 = []
		IR3.append("MATCH " + ",\n ".join(IR2["MATCH"]))
		IR3.append("\n")
		if IR2["WHERE"]:
			IR3.append("WHERE " + "\n AND ".join(IR2["WHERE"]))
			IR3.append("\n")
		IR3.append("RETURN " + ",\n ".join(IR2["RETURN"]))
		IR3.append("\n")
		IR3.append("LIMIT " + str(IR2["LIMIT"]))

		IR3 = ''.join(IR3)
		return IR3

	def execute(self,query):
		return self.db.execute(query)
	
	def simply_query(self,query):
		return self.db.simply_query(query)

	def build(self, IR1):

		try:
			IR2 = self.build_stage_1(IR1)
		except Exception, e:
			return {"query": None, "message": str(e)}

		query = self.build_stage_2(IR2)
		
		print "=" * 30 + "QUERY" + "=" * 30
		print query
		
		return {"query": query}

		

if __name__ == '__main__':
	
	b = Builder()
	IR1 = { 
		"location": "Bangalore Division",
		"rating": {"min": 3, "max": 5, "exact": None},
		"amenities": ["WiFi","Gym","Cafe"],
		"roomtype":{
			"any":{
				"cost":{
					"min": 1000,
					"max": 12000,
					"exact": None,
				},
				"children": 4,
				"adults": 6,
		 	},
		},
		"limit" : 25
	}
	
	query = b.build(IR1)

	if query["query"]:	
		resultset = b.simply_query(query["query"])
		fmtr = Formatter()
		print fmtr.format(resultset)
