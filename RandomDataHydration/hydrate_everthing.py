from py2neo import watch, authenticate, Graph
import json, time

"""
Quick and dirty code to hydrate Neo4j Database
from the json files.
"""
tic = time.time()

watch('httpstream')
authenticate('localhost:7474','neo4j','Tr!pC0rr!d0r')
graph = Graph()
graph.delete_all()

tuples = []
def unfold(my_dict, prefix = ''):
    global tuples
    if prefix:
        prefix += '_'
    print "my_dict: ", my_dict
    for k, v in my_dict.items():
        if not isinstance(v, dict):
                tuples.append((prefix+k,v))
        else:
            for k2, v2 in v.items():
                if isinstance(v2, dict):
                    unfold(v2,prefix=prefix+k+'_'+k2)
                else:
                    tuples.append((prefix+k+'_'+k2,v2))

def build_neo4j_json(my_json):
    global tuples
    tuples = []
    unfold(my_json)
    my_json = dict(tuples)

    dump = json.dumps(my_json, indent = 4)
    marked = []

    dump = dump.decode().encode('ascii','ignore')
    state = 0
    i = 0
    while i < len(dump) - 1:
        if dump[i] == '"' and state == 0:
            marked.append(i)
        if dump[i] == '"' and state == 1:
            if dump[i+1] == ':':
                marked.append(i)
            else:
                marked.pop()

        if dump[i] == '"':
            state = 1 - state

        i += 1
    dump2 = ''.join((d for i,d in enumerate(dump) if not i in marked)) 
    return dump2

print """ LET THE WAR BEGIN >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
======================================================================
"""

print 'Creating country India...'
statement = """
MERGE (c:Country {name: 'India', capital: 'Delhi', continent: 'Asia'})
RETURN c"""
print graph.cypher.execute(statement)

states = json.load(open('Original/karnataka.json','r'))
for state in states:
    statement = """
    MERGE (s:State %s)
    RETURN s
    """ % build_neo4j_json(state)
    print "Creating state: executing statement...", statement
    print graph.cypher.execute(statement)

    print 'Creating relation (India)-->(State)...'
    statement2 = """
    MATCH (c:Country),(s:State)
    WHERE c.name = "%s" AND s.name = "%s" 
    MERGE (c)-[:HAS]->(s)
    RETURN s""" % ("India", state['name'])
    print graph.cypher.execute(statement2)

direct_destinations = json.load(open('Fake/direct_destinations2.json','r'))
for dd in direct_destinations:
    categories = dd.pop('categories')
    state = "Karnataka"
    statement = """MERGE (dd:DirectDestination %s)
    RETURN dd""" % build_neo4j_json(dd)
    print 'statement: ', statement
    result = graph.cypher.execute(statement)
    statement2 = """
    MATCH (s:State),(dd:DirectDestination)
    WHERE s.name = "%s" AND dd.name = "%s" 
    MERGE (s)-[:HAS {categories: %s }]->(dd)
    """ % (state, dd['name'], map(str,categories))
    print 'statement2: ', statement2
    print graph.cypher.execute(statement2)


major_destinations = json.load(open('Original/major_destinations.json','r'))
for md in major_destinations:
    categories = md.pop('categories')
    state = "Karnataka"
    statement = """MERGE (md:MajorDestination %s)
    RETURN md""" % build_neo4j_json(md)
    print 'statement: ', statement
    result = graph.cypher.execute(statement)
    statement2 = """
    MATCH (s:State),(md:MajorDestination)
    WHERE s.name = "%s" AND md.name = "%s" 
    MERGE (s)-[:HAS {categories: %s }]->(md)
    """ % (state, md['name'], map(str,categories))
    print 'statement2: ', statement2
    print graph.cypher.execute(statement2) 


points_of_interest = json.load(open('Fake/point_of_interest2.json','r'))
print 'Inserting points_of_interest...'
pasfs = {}

for poi in points_of_interest:
    md = None
    if poi.has_key('point_of_interest_in'):
        md = poi.pop('point_of_interest_in')
    pasfs[poi['name']] = []
    if poi.has_key('people_also_searched_for'):
        pasfs[poi['name']] = poi.pop('people_also_searched_for')

    statement = """MERGE (poi:PointOfInterest %s)
    RETURN poi""" % build_neo4j_json(poi)
    print 'statement: ', statement
    result = graph.cypher.execute(statement)

    if not md or "Karnataka" in md:
        statement2 = """
        MATCH (poi:PointOfInterest),(s:State)
        WHERE poi.name = "%s" AND s.name = "%s" 
        MERGE (s)-[:HAS]->(poi)
        """ % (poi['name'], "Karnataka") 
        print 'statement2: ', statement2
        print graph.cypher.execute(statement2) 
    else:
        for md_elem in md:
            statement2 = """
            MATCH (poi:PointOfInterest),(md:MajorDestination)
            WHERE poi.name = "%s" AND md.name = "%s" 
            MERGE (md)-[:HAS]->(poi)
            """ % (poi['name'], md_elem)
            print 'statement2: ', statement2
            print graph.cypher.execute(statement2) 

print "Creating PASF relations..."
for poi, pasf in pasfs.items():
    for other in pasf:
        poi2 = other['point_of_interest']
        rank = other['rank']

        statement2 = """
        MATCH (poi:PointOfInterest),(poi2:PointOfInterest)
        WHERE poi.name = "%s" AND poi2.name = "%s"
        MERGE (poi)-[:PASF {rank: %d}]->(poi2)
        """ % (poi,poi2,rank)
        print 'statement2: ', statement2
        print graph.cypher.execute(statement2)

addresses = json.load(open('Original/addresses.json','r'))
for address in addresses:
    address.pop('country')
    address.pop('state')
    statement = """
    MERGE (d:District %s)
    RETURN d
    """ % build_neo4j_json(address)
    print 'statement2: ', statement
    print graph.cypher.execute(statement)

    statement2 = """
    MATCH (d:District),(s:State)
    WHERE d.district = "%s" AND d.subdistrict = "%s" AND s.name = "%s"
    MERGE (s)-[:ADDR]->(d)
    """ % (address['district'],address['subdistrict'], "Karnataka")
    print 'statement2: ', statement2
    print graph.cypher.execute(statement2)

hotels = json.load(open('Fake/hotels2.json','r'))
for hotel in hotels:
    statement = """
    MERGE (h:Hotel %s)
    RETURN h
    """ % build_neo4j_json(hotel)
    print 'statement: ', statement
    print graph.cypher.execute(statement)

    statement2 = """
    MATCH (h:Hotel),(s:State)
    WHERE h.name = "%s" AND s.name = "%s"
    MERGE (s)-[:HOTEL]->(h)
    """ % (hotel['name'], "Karnataka")
    print 'statement2: ', statement2
    print graph.cypher.execute(statement2)


###FUNNY BIT
print " THE WAR HAS COME TO AN END. THANKS FOR WATCHING THIS MOVIE"
print "=" * 80

toc = time.time()

print "You watched this movie for %d seconds" % (toc - tic)
