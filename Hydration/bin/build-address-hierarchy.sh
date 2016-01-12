#!/bin/bash
# if [ $# -eq 0 ]; then
# 	echo "Usage: build-address-hierarchy.sh </path/to/Hydration/data>"
# 	echo "Example: ./build-address-hierarchy /home/mushtaque/TC/Hydration/data"
# 	exit 1
# fi

#good demonstartion of UNIX pipe and filter below!

alt=`pwd | rev | cut -d "/" -f 2- | rev`"/data"
wtf=`echo "${1:-$alt}" | sed 's:[/\\&]:\\?:g'` # I sed wtf! Ha Haa!

time cat ../utils/address-hierarchy-quick-and-dirty.cql | \
sed "s/XXX/$wtf/g" | tr "?" "/" | \
/var/lib/neo4j/bin/neo4j-shell -file -

echo "Built Address Heirarchy Successfully."
echo "Scroll up to see Warnings (if any then take action accordingly)."

#phew. sooo.. cryptic indeed. seven pipes used up.