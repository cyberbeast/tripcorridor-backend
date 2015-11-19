import json, random

INFILE = "Original/hotels.json"
OUTFILE = "Original/hotels2.json"


data = json.load(open(INFILE,'r'))

def process(datum, index):
	datum['id'] = index + 1

	child_cost = random.randint(5,200) * 100 + random.randint(0,10) * 10
	adult_cost = int((child_cost) * (1 + random.randint(0,10) * 3.0 / 40.0))
	pricing = { 
		"adult": 
			{ 
				"min" : random.randint(1,3),
				"max" : random.randint(2,10),
				"cost_per_night" : adult_cost
			},
		"child":
			{
				"min" : random.randint(1,3),
				"max" : random.randint(2,10),
				"cost_per_night" : child_cost
			}
	}
	datum['pricing'] = pricing
	
	if datum['rating'] == "NA":
		datum['rating'] = random.randint(1,101)

	return datum

for index, datum in enumerate(data):
	data[index] = process(datum, index)

json.dump(data, open(OUTFILE,'w'), indent = 4)