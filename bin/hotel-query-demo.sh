#!/bin/bash

# this script is used to query the model 
# by passing it a quoted natural language query

echo "Demo-ing hotel query"
request='{
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
	}'

#request=`echo $request | sed 's/"/\\\\"/g' `
#request='\"a\":\"hello\"'

curl -i -u mushtaque:secret -H "Content-Type: application/json" \
	-X POST -d "$request" http://localhost:6000/api/naturalquery/execute