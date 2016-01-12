import json, sys, os

filename = sys.argv[1]
basename = os.path.splitext(filename)[0]

data = json.load(open(filename,'r'))

print "basename", basename
with open(basename + '.csv','w') as csvfile:
	for key in data:
		for elem in data[key]:
			csvfile.write(key + "," + elem + "\n") 

;; # so that you can't run this directly