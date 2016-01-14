MATCH (n:RoomType) DETACH DELETE n;
MATCH (n:Rating) DETACH DELETE n;
MATCH (n:Amenity) DETACH DELETE n;
MATCH (n:Hotel) DETACH DELETE n;

CREATE (r:RoomType{type:"Standard A/C Room"});
CREATE (r:RoomType{type:"Standard Non A/C Room"});
CREATE (r:RoomType{type:"Deluxe"});
CREATE (r:RoomType{type:"Suite"});

CREATE (r:Rating{scale:3});
CREATE (r:Rating{scale:4});
CREATE (r:Rating{scale:5});
CREATE (r:Rating{scale:7});

CREATE (a:Amenity{name:"Air Conditioned"});
CREATE (a:Amenity{name:"Room Service"});
CREATE (a:Amenity{name:"Swimming Pool"});
CREATE (a:Amenity{name:"Bar"});
CREATE (a:Amenity{name:"Gym"});
CREATE (a:Amenity{name:"Business Center"});
CREATE (a:Amenity{name:"Restaurant"});
CREATE (a:Amenity{name:"WiFi"});
CREATE (a:Amenity{name:"Internet"});
CREATE (a:Amenity{name:"Cafe"});

// add hotels; 
LOAD CSV WITH HEADERS FROM 
'file://XXX/hotels.tsv' AS hotel
FIELDTERMINATOR "\t"
CREATE (h:Hotel{name:hotel.name, id: toInt(hotel.id)});

// link hotels with rating;
LOAD CSV WITH HEADERS FROM 
'file://XXX/hotels.tsv' AS hotel
FIELDTERMINATOR "\t"
MATCH (h:Hotel),(r:Rating)
WHERE h.id = toInt(hotel.id) AND r.scale = toInt(hotel.rating)
CREATE (h)-[:HAS_RATING]->(r);

// link hotel with its district from address hierarchy;
LOAD CSV WITH HEADERS FROM 
'file://XXX/hotels.tsv' AS hotel
FIELDTERMINATOR "\t"
MATCH (h:Hotel),(d:District)
WHERE h.id = toInt(hotel.id) AND d.name = hotel.district
CREATE (d)-[:HAS_HOTEL]->(h);

// link hotels with amenities;
LOAD CSV WITH HEADERS FROM 
'file://XXX/amenities.tsv' AS amenity
FIELDTERMINATOR "\t"
MATCH (h:Hotel),(a:Amenity)
WHERE h.id = toInt(amenity.id) AND a.name = amenity.amenity
CREATE (h)-[:HAS_AMENITY]->(a);

// link hotels with room type;
LOAD CSV WITH HEADERS FROM 
'file://XXX/roomtype.tsv' AS rt
FIELDTERMINATOR "\t"
MATCH (h:Hotel), (r:RoomType)
WHERE h.id = toInt(rt.id) AND r.type = rt.roomtype
CREATE (h)-[:HAS_ROOMTYPE{cost:toInt(rt.cost),max_adults:toInt(rt.max_adults),
	max_children:toInt(rt.max_children),duration:toInt(rt.duration)}]->(r);






