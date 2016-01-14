locations = ["India","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar",
"Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir",
"Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur",
"Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim",
"Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
"Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu",
"Lakshadweep","National Capital Territory of Delhi","Puducherry","North India",
"East India","Western India","South India","Northeast India","Bagalkot","Bellary",
"Belgaum","Bangalore Rural","Bangalore Urban","Bidar","Chamarajnagar","Chikkaballapur",
"Chikkamagaluru","Chitradurga","Dakshina Kannada","Davanagere","Dharwad","Gadag",
"Hassan","Haveri","Gulbarga","Kodagu","Kolar","Koppal","Mandya","Mysore","Raichur",
"Ramanagara","Shimoga","Tumkur","Udupi","Uttara Kannada","Vijayapura","Yadgir",
"Belgaum Division","Kalaburagi Division","Bangalore Division","Mysore Division"]


from geopy import GoogleV3,exc 
import json

geocoder = GoogleV3()
filename = "geocoded-locations.tsv"

geocodeds = []
for location in locations:
	geocoded = {"name":location}
	try:
		print 'trying... ',  location
		data = geocoder.geocode(location,timeout = 10)
	except exc.GeocoderQuotaExceeded:
		print 'exc.GeocoderQuotaExceeded'
		break

	if data != None:
		print data.latitude, data.longitude
		geocoded['latitude'] = data.latitude
		geocoded['longitude'] = data.longitude
	else:
		print "none returned by google"
	geocodeds.append(geocoded)
	

with open(filename,'w') as outfile:
	json.dump(geocodeds,outfile,indent = 4)
	