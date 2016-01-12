//QUICK AND DIRTY CODE TO HYDRATE THE DATABASE                   ;
//Run the script as                                              ;
//$ cd /path/to/cql/script                                       ;
//$ /var/lib/neo4j/bin/neo4j-shell -file <this-cql-scirpt-name>  ;
//NOTE: the file://XXX must be changed to                        ;
//file://<path/to/your/data> below, before execution of this     ;
//script. So better run  Hydration/bin/build-address-hierarchy.sh;

MATCH (n) DETACH DELETE n // clean database everytime;

//add country;
CREATE (c:Country{name:"India",currency:"INR",
	code:"IN",capital:"New Delhi"});

//add states;
LOAD CSV WITH HEADERS FROM 
'file://XXX/states.tsv' AS state
FIELDTERMINATOR "\t"
CREATE (s:State{name:state.Name, number:toInt(state.Number), 
	code:state.Code, capital:state.Capital});

//link states to country;
MATCH (c:Country),(s:State)
WHERE c.name = "India"
CREATE (c)-[r:HAS_STATE]->(s);

//add union territories;
LOAD CSV WITH HEADERS FROM 
'file://XXX/union-territories.tsv' 
AS ut FIELDTERMINATOR "\t"
CREATE (u:UnionTerritory{name:ut.UnionTerritory, 
	number:ut.Number, code:ut.Code, capital:ut.Capital});

//link union territories to country;
MATCH (c:Country),(ut:UnionTerritory)
WHERE c.name = "India"
CREATE (c)-[r:HAS_UNION_TERRITORY]->(ut);

//add regions;
CREATE (r:Region{name:"North India"});
CREATE (r:Region{name:"East India"});
CREATE (r:Region{name:"Western India"});
CREATE (r:Region{name:"South India"});
CREATE (r:Region{name:"Northeast India"});

//link regions to country
MATCH (c:Country),(r:Region)
WHERE c.name = "India"
CREATE (c)-[:HAS_REGION]->(r);

//link region with states and union territories;
LOAD CSV WITH HEADERS FROM 
'file://XXX/regions-of-india.csv' 
AS region
MATCH (r:Region),(state_or_ut)
WHERE r.name = region.Name AND state_or_ut.name = region.State
CREATE (r)-[:HAS_STATE_OR_UNION_TERRITORY]->(state_or_ut);

//add districts of Karnataka;
LOAD CSV WITH HEADERS FROM 
'file://XXX/districts-of-karnataka.tsv' 
AS district FIELDTERMINATOR '\t'
CREATE (d:District{name:district.District,
	code:district.Code,headquarter:district.Headquarters});

//link districts of Karnataka to Karnataka;
MATCH (s:State),(d:District)
WHERE s.name = "Karnataka"
CREATE (s)-[:HAS_DISTRICT]->(d);

//add divisions to Karnataka;
CREATE (div:Division{name:"Belgaum Division"});
CREATE (div:Division{name:"Kalaburagi Division"});
CREATE (div:Division{name:"Bangalore Division"});
CREATE (div:Division{name:"Mysore Division"});

//link divisions of Karnataka to Karnataka;
MATCH (s:State),(div:Division)
WHERE s.name = "Karnataka"
CREATE (s)-[:HAS_DIVISION]->(div);

//link divisions to district in Karnataka;
LOAD CSV WITH HEADERS FROM 
'file://XXX/divisions-of-karnataka.csv' 
AS div
MATCH (d:Division),(dis:District)
WHERE d.name = div.Name AND dis.name = div.District
CREATE (d)-[:HAS_DISTRICT_UNDER_DIVISION]->(dis);
