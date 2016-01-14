#!/bin/bash

alt=`pwd | rev | cut -d "/" -f 2- | rev`"/data"
wtf=`echo "${1:-$alt}" | sed 's:[/\\&]:\\?:g'` # I sed wtf! Ha Haa!

time cat ./add-lat-lng.cql | \
sed "s/XXX/$wtf/g" | tr "?" "/" | \
/var/lib/neo4j/bin/neo4j-shell -file -

echo "Geocoded all locations and hotels successfully."
echo "Scroll up to see Warnings (if any then take action accordingly)."