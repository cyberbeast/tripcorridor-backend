#!/bin/bash

# this script is used to query the model 
# by passing it a quoted natural language query

if [ $# -eq 0 ]; then 
	echo "usage: query.sh <quoted natural language query> "
	exit
fi
echo "natural language query: \"$1\" "

curl -i -u mushtaque:secret -H "Content-Type: application/json" \
-X POST -d "{ \"query\": \"$1\"}" http://localhost:6000/api/naturalquery/execute