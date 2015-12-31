"""
    All global setting for TripCorridor is done here.
"""
NLTK_DATA_PATH = ["/home/ubuntu/NLP/nltk_data",
				"/home/mushtaque/nltk_data"]


LOG_FILE = "log.txt"
LOG = True
LOG_DIR = "logs"


NEO4J_DB_URI = "http://localhost:7474/db/graph" #deprecated not used anymore

NEO4J_DB_URL_PORT = "localhost:7474"
NEO4J_DB_USERNAME = "neo4j"
NEO4J_DB_PASSWORD = "Tr!pC0rr!d0r" # "neo4j123"  #"Tr!pC0rr!d0r"

FAKE_DB_ACCESS = False #set this to true, when DB is not yet up and running.
#use FAKE_DB_ACCESS for testing API only. For Proper operation check
#that Neo4j DB is running and then this value to False.
API_USERNAME = "mushtaque"
API_KEY = "secret"


