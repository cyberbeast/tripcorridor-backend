#!/bin/bash
./restart-neo4j-db.sh
./build-address-hierarchy.sh
./add-hotels.sh
./add-lat-lng.sh

