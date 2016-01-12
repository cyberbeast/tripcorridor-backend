#!/bin/bash

echo "Proxy client querying NaturalQuery API"

# query="Hotels in Mysore less than rupees 5000 for 3 people and 4 children"

# query="`echo $query | sed 's/ /%20/g'`"

# request="curl -H 'Authorization: Bearer CWKXT3S2LBBS3DDRXCYR6SHOUPSTSGPW' 'https://api.wit.ai/message?=20160107&q=${query}'"

# echo $request

# response=`$request`

# echo "Response: "
# echo $response
request='{
    "wit_ai_response": {
        "outcomes": [
            {
                "entities": {
                    "location": [
                        {
                            "suggested": true, 
                            "type": "value", 
                            "value": "Dubai"
                        }
                    ]
                }, 
                "confidence": 0.908, 
                "intent": "hotel_discovery", 
                "_text": "Business Hotels in Dubai"
            }
        ], 
        "msg_id": "59b45508-5355-4145-9c17-6ac120ff47ba", 
        "_text": "Business Hotels in Dubai"
    }
}'

set -x

curl -i -u TripCorridor:NjQwNzlkNmI1MWI5YWI3YjVjODM0Yjc2YzFkN2I4YjNlMWI5YmMyYw== \
-H "Content-Type: application/json" \
-X POST -d "$request" http://localhost:5544/api/naturalquery/execute