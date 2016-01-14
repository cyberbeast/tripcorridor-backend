LOAD CSV WITH HEADERS FROM 
'file://XXX/geocoded-hotel.tsv' AS hotel
FIELDTERMINATOR "\t"
MATCH (h:Hotel)
WHERE h.name = hotel.name
SET h.latitude = toFloat(hotel.latitude)
SET h.longitude = toFloat(hotel.longitude)
RETURN h;

LOAD CSV WITH HEADERS FROM 
'file://XXX/geocoded-locations.tsv' AS location
FIELDTERMINATOR "\t"
MATCH (l:Location)
WHERE l.name = location.name
SET l.latitude = toFloat(location.latitude)
SET l.longitude = toFloat(location.longitude)
RETURN l;