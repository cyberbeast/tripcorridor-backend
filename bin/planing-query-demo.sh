#!/bin/bash

# this script is used to query the model 
# by passing it a quoted natural language query

echo "Demo-ing planning query"
request='{
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
	}'

#request=`echo $request | sed 's/"/\\\\"/g' `
#request='\"a\":\"hello\"'

curl -i -u mushtaque:secret -H "Content-Type: application/json" \
	-X POST -d "$request" http://localhost:6000/api/naturalquery/execute