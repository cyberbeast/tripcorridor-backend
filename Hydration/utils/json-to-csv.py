import json, sys, os, csv

filename = sys.argv[1]
basename = os.path.splitext(filename)[0]

data = json.load(open(filename,'r'))
headers = ["name","latitude","longitude"]

print "basename", basename
dict_writer = csv.DictWriter(open(basename + '.csv', 'w'), 
	fieldnames = headers, delimiter = "\t")

dict_writer.writeheader()
for obj in data:
	dict_writer.writerow(obj)
	

;; # so that you can't run this directly