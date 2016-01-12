import json, subprocess, os, time, sys

class WitAI(object):

	@staticmethod
	def query(query):

		query = query.replace(' ','%20')

		curl_req = """curl -H \
		'Authorization: Bearer CWKXT3S2LBBS3DDRXCYR6SHOUPSTSGPW'\
	  	'https://api.wit.ai/message?=%s&q=%s' """

	  	t = time.localtime()
	  	today = ("%d%2d%2d" % (t.tm_year,t.tm_mon,t.tm_mday)).replace(' ','0')
	  	

	  	FNULL = open(os.devnull,'w')
		proc = subprocess.Popen(curl_req % (today,query),
		stdout=subprocess.PIPE, stderr=FNULL, shell=True)
		(out, err) = proc.communicate()

		print "QUERY:"
		print curl_req % (today,query)
		
		print "wit.ai OUTPUT:"
		print out
		
		return json.loads(out)

if __name__ == '__main__':

	query = "Hotels in Mysore less than rupees 5000 for 3 people and 4 children"
	if len(sys.argv) > 1:
		query = sys.argv[1]
	print "INPUT:", query
	out = WitAI.query(query)

	print "OUTPUT:"
	print json.dumps(out, indent = 4)