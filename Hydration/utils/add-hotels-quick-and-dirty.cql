MATCH (n:RoomType) DETACH DELETE n;
MATCH (n:Rating) DETACH DELETE n;
MATCH (n:Amentity) DETACH DELETE n;
MATCH (n:Hotel) DETACH DELETE n;

CREATE (r:RoomType{type:"Standard A/C Room"});
CREATE (r:RoomType{type:"Standard Non A/C Room"});
CREATE (r:RoomType{type:"Deluxe"});
CREATE (r:RoomType{type:"Suite"});

CREATE (r:Rating{scale:3});
CREATE (r:Rating{scale:4});
CREATE (r:Rating{scale:5});
CREATE (r:Rating{scale:7});

CREATE (a:Amentity{name:"Air Conditioned"});
CREATE (a:Amentity{name:"Room Service"});
CREATE (a:Amentity{name:"Swimming Pool"});
CREATE (a:Amentity{name:"Bar"});
CREATE (a:Amentity{name:"Gym"});
CREATE (a:Amentity{name:"Business Center"});
CREATE (a:Amentity{name:"Restaurant"});
CREATE (a:Amentity{name:"WiFi"});
CREATE (a:Amentity{name:"Internet"});
CREATE (a:Amentity{name:"Cafe"});


// add hotels; 
LOAD CSV WITH HEADERS FROM 
'file://XXX/hotels.tsv' AS hotel
FIELDTERMINATOR "\t"
CREATE (h:Hotel{name:hotel.name, id:hotel.id});

// link hotels with rating;
LOAD CSV WITH HEADERS FROM 
'file://XXX/hotels.tsv' AS hotel
FIELDTERMINATOR "\t"
MATCH (h:Hotel),(r:Rating)
WHERE h.id = hotel.id AND r.scale = hotel.rating
CREATE (h)-[:HAS_RATING]->(r);

// link hotel with its district from address hierarchy;
LOAD CSV WITH HEADERS FROM 
'file://XXX/hotels.tsv' AS hotel
FIELDTERMINATOR "\t"
MATCH (h:Hotel),(d:District)
WHERE h.id = hotel.id AND d.name = hotel.district
CREATE (d)-[:HAS_HOTEL]->(h);

// link hotels with amenities;
LOAD CSV WITH HEADERS FROM 
'file://XXX/amenities.tsv' AS amenity
FIELDTERMINATOR "\t"
MATCH (h:Hotel),(a:Amentity)
WHERE h.id = amenity.id AND a.name = amenity.amenity
CREATE (h)-[:HAS_AMENITY]->(a);

// link hotels with room type;
LOAD CSV WITH HEADERS FROM 
'file://XXX/roomtype.tsv' AS rt
FIELDTERMINATOR "\t"
MATCH (h:Hotel), (r:RoomType)
WHERE h.id = rt.id AND r.type = rt.roomtype
CREATE (h)-[:HAS_ROOMTYPE{cost:toInt(rt.cost),max_adults:toInt(rt.max_adults),
	max_children:toInt(rt.max_children),duration:toInt(rt.duration)}]->(r);






