#!/bin/bash

# this script is to start neo4j server and 
# the flask api for natural language query

echo "starting neo4j server..."
sudo /var/lib/neo4j/bin/neo4j restart

echo "starting flask app at localhost:6000/api/naturalquery/execute ..."
python ../QueryGeneration/api.py 