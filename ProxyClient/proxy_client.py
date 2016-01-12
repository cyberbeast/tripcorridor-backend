from witai import WitAI 
import os, json, subprocess, sys

class ProxyClient(object):

	@staticmethod
	def query(wit_ai_response):

		url = "http://localhost:5544/api/naturalquery/execute"
		header = "Content-Type: application/json"
		api_user_name = "TripCorridor"
		api_key = "NjQwNzlkNmI1MWI5YWI3YjVjODM0Yjc2YzFkN2I4YjNlMWI5YmMyYw=="

		curl_request = """curl -i -u %s:%s -H "%s" -X POST -d '%s' %s """ % \
		(api_user_name,api_key,header,wit_ai_response,url)

	  	FNULL = open(os.devnull,'w')
		proc = subprocess.Popen(curl_request,
		stdout=subprocess.PIPE, stderr=FNULL, shell=True)
		(out, err) = proc.communicate()

		return out

if __name__ == '__main__':

	query = "Business Hotels in Dubai"
	if len(sys.argv) >= 2:
		query = sys.argv[1]

	wit_ai_response = {"wit_ai_response": WitAI.query(query)}

	response = ProxyClient.query(json.dumps(wit_ai_response, indent = 4))

	print "=" * 30 + "RESPONSE" + "=" * 30
	if response:
		print response
	else:
		print "Natural Query API is down!!"
		print "Check whether Flask API server at port 5544 is running."