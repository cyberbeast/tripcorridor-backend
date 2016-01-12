"""
    All global setting for TripCorridor is done here.
"""
import base64
NLTK_DATA_PATH = ["/home/ubuntu/NLP/nltk_data",
				"/home/%s/nltk_data" % base64.b64decode('bXVzaHRhcXVl') ]
#I just diguised my name in base64! Ha Ha Ha! 
#Don't worry unless your CIA or FBI 

LOG_FILE = "log.txt"
LOG = True
LOG_DIR = "logs"

NEO4J_DB_URI = "http://localhost:7474/db/graph" #deprecated not used anymore

NEO4J_DB_URL_PORT = "localhost:7474"
NEO4J_DB_USERNAME = "neo4j"

import os

if os.getlogin() ==  base64.b64decode('bXVzaHRhcXVl'):
	NEO4J_DB_PASSWORD = "neo4j123"  
else:
	NEO4J_DB_PASSWORD = "Tr!pC0rr!d0r"

FAKE_DB_ACCESS = False #set this to true, when DB is not yet up and running.
#use FAKE_DB_ACCESS for testing API only. For Proper operation check
#that Neo4j DB is running and then this value to False.

#API settings
API_USERNAME = "TripCorridor"
API_KEY = "NjQwNzlkNmI1MWI5YWI3YjVjODM0Yjc2YzFkN2I4YjNlMWI5YmMyYw=="
API_PORT = 5544
API_HOST_IP_ADDRESS = "0.0.0.0"

#NOTE: api key in generated from api username as its sha-1 digest, 
#and the encoded in base64. Don't rely on the API_KEY above.
#
#import hashlib, base64 
#sha1_hash = hashlib.sha1(.API_USERNAME).hexdigest()
#API_KEY = base64.b64encode(sha1_hash)
