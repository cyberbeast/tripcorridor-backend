parsed_args = { "wit_ai_response": {
    "outcomes": [
        {
            "entities": {
            	"location": [
                    {
                        "suggested": True, 
                        "type": "value", 
                        "value": "Bengaluru"
                    }
                ],

                "accomodation_room_type": [
                    {
                        "suggested": True, 
                        "entities": { "whatever" : [[{
                            "accomodation_amenity": [
                                {
                                    "type": "value", 
                                    "value": "WiFi"
                                }, 
                                {
                                    "type": "value", 
                                    "value": "Bar"
                                }, 
                                {
                                    "type": "value", 
                                    "value": "Gym"
                                }
                            ]
                        }]]}, 
                        "type": "value", 
                        "value": "wifi gym and bar"
                    }
                ]
            }, 
            "confidence": 0.935, 
            "intent": "hotel_discovery", 
            "_text": "Hotels with wifi gym and bar"
        }
    ], 
    "msg_id": "4562f5c5-df23-4303-98cb-3e1acc5ece34", 
    "_text": "Hotels with wifi gym and bar"
}
}

IR1 = { 
	"location": "Bangalore Division",
	"rating": {"min": 3, "max": 5, "exact": None},
	"amenities": ["WiFi","Gym","Cafe"],
	"roomtype":{
		"any":{
			"cost":{
				"min": 1000,
				"max": 12000,
				"exact": None,
			},
			"children": 4,
			"adults": 6,
	 	},
	},
	"limit" : 3
}
	