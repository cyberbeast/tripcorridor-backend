import json, random

INFILE = "Original/direct_destinations.json"
OUTFILE = "Original/direct_destinations2.json"


data = json.load(open(INFILE,'r'))
entities = json.load(open('entities.json','r'))
seasons = entities['season']
months = entities['month']


def process(datum, index):
	datum['id'] = index + 1

	if not datum.has_key('categories'):
		datum['categories'] = ['All Destinations']
	
	datum['best_season'] = { 'from': random.choice(months),
	'to': random.choice(months)}
	
	return datum

for index, datum in enumerate(data):
	data[index] = process(datum, index)

json.dump(data, open(OUTFILE,'w'), indent = 4)