import json, sys

class RequestProcessor(object):
	
	def __init__(self,request):
		self.intent = request["intent"]
		self.query = request["query"]
		self.entities = request["entities"]

	def __repr__(self):
		return """
		request processor:
			intent: %s
			query: %s
			entities: %s
		""" %

def main(): 
	request = json.loads(sys.argv[1])
	rp = RequestProcessor(request)
	print rp 

if __name__ == '__main__':
	main()