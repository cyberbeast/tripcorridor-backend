#!/bin/bash
alt=`pwd | rev | cut -d "/" -f 2- | rev`"/data"
wtf=`echo "${1:-$alt}" | sed 's:[/\\&]:\\?:g'` # I sed wtf! Ha Haa!

time cat ../utils/add-hotels-quick-and-dirty.cql | \
sed "s/XXX/$wtf/g" | tr "?" "/" | \
/var/lib/neo4j/bin/neo4j-shell -file -

echo "Added Hotels Successfully."
echo "Scroll up to see Warnings (if any then take action accordingly)."