import base64, os

NEO4J_DB_URL_PORT = "localhost:7474"
NEO4J_DB_USERNAME = "neo4j"

if os.getlogin() ==  base64.b64decode('bXVzaHRhcXVl'):
	NEO4J_DB_PASSWORD = "neo4j123"  
else:
	NEO4J_DB_PASSWORD = "Tr!pC0rr!d0r"

API_USERNAME = "TripCorridor"
API_KEY = "NjQwNzlkNmI1MWI5YWI3YjVjODM0Yjc2YzFkN2I4YjNlMWI5YmMyYw=="
API_PORT = 5544
API_HOST_IP_ADDRESS = "0.0.0.0"

#NOTE: api key in generated from api username as its sha-1 digest, 
#	and the encoded in base64. Don't rely on the API_KEY above. In code,
#	that is as follows 
#import hashlib, base64 
#sha1_hash = hashlib.sha1(API_USERNAME).hexdigest()
#API_KEY = base64.b64encode(sha1_hash)
