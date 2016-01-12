import json, csv, random, numpy as np

hotels = json.load(open("/home/mushtaque/TC/Hydration/data/hotels.json","r"))
names = [hotel["name"] for hotel in hotels]

names = [name.encode("ascii","ignore") for name in names]
districts = ["Bagalkot","Bellary","Belgaum","Bangalore Rural","Bangalore Urban",
"Bidar","Chamarajnagar","Chikkaballapur","Chikkamagaluru","Chitradurga",
"Dakshina Kannada","Davanagere","Dharwad","Gadag","Hassan","Haveri",
"Gulbarga","Kodagu","Kolar","Koppal","Mandya","Mysore","Raichur","Ramanagara",
"Shimoga","Tumkur","Udupi","Uttara Kannada","Vijayapura","Yadgir"]

room_types = ["Standard A/C Room","Standard Non A/C Room",
"Deluxe","Suite"]

ratings = [3,4,5,7]
rating_probs = np.array([50.0,10.0,30.0,10.0])

amenities = ["Air Conditioned","Room Service","Swimming Pool","Bar",
"Gym","Business Center","Restaurant","WiFi","Internet","Cafe"]

hotels = []
for i in range(len(names)):
	hotel = {"id":i}
	hotel["name"] = names[i]
	hotel["district"] = random.choice(districts)
	hotel["rating"] = np.random.choice(ratings,p = rating_probs/sum(rating_probs))
	hotels.append(hotel)

#print hotels

csvfile = open("/home/mushtaque/TC/Hydration/data/hotels.tsv",'w')
#print float(len([hotel for hotel in hotels if hotel["rating"] == 5]))/len(hotels)
headers = ["id","name","district","rating"]
writer = csv.DictWriter(csvfile, fieldnames = headers, delimiter = "\t")

writer.writeheader()
for row in hotels:
	writer.writerow(row)


csvfile = open("/home/mushtaque/TC/Hydration/data/amenities.tsv",'w')

writer = csv.writer(csvfile, delimiter = "\t")
writer.writerow(["id","amenity"])

for row in hotels:
	sampled_amenities = random.sample(amenities,random.randint(0,len(amenities)))
	for sample in sampled_amenities:
		the_row = row["id"], sample
		#print the_row
		writer.writerow(the_row)

joe1, joe2 = [], {}
for hotel in hotels:
	rooms = random.sample(room_types, random.randint(1,len(room_types)))
	for room in rooms:
		joe2 = {"id": hotel["id"],"roomtype":room}
		joe2["cost"] = random.randint(0,38000)
		joe2["max_adults"] = random.randint(2,10)
		joe2["max_children"] = random.randint(0,10)
		joe2["duration"] = 24
		joe1.append(joe2)

#print joe1, len(joe1)


csvfile = open("/home/mushtaque/TC/Hydration/data/roomtype.tsv",'w')
headers = ["id","roomtype","cost","max_adults","max_children","duration"]
writer = csv.DictWriter(csvfile, fieldnames = headers, delimiter = "\t")

writer.writeheader()
for row in joe1:
	writer.writerow(row)

;; #you know
# that is joe programming. :p