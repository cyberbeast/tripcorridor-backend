import json, random

INFILE = "Original/point_of_interest.json"
OUTFILE = "Original/point_of_interest2.json"


data = json.load(open(INFILE,'r'))
entities = json.load(open('entities.json','r'))
seasons = entities['season']
months = entities['month']


def process(datum, index):
	datum['id'] = index + 1
	
	datum['best_season'] = { 'from': random.choice(months),
	'to': random.choice(months)}
	
	datum['timings'] = { 'from': random.randint(6,11),
	'to': random.randint(12,20)}

	child_ticket = random.randint(1,10) * 100 + random.randint(1,4) * 25
	datum['pricing'] = { 'child': child_ticket,
	  'adult': child_ticket + random.randint(0,3) * 100 + random.randint(1,4) * 25}
	return datum

for index, datum in enumerate(data):
	data[index] = process(datum, index)

json.dump(data, open(OUTFILE,'w'), indent = 4)