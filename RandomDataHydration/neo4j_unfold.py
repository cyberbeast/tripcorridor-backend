
hotel = {
        "rating": "NA", 
        "name": "Dasharath", 
        "longitude": 76.6393805, 
        "pricing": {
            "adult": {
                "max": 7, 
                "cost_per_night": 47409, 
                "min": 1
            }, 
            "child": {
                "max": 3, 
                "cost_per_night": 7909, 
                "min": 1
            }
        }, 
        "address": "Mysore, Karnataka, India", 
        "latitude": 12.2958104, 
        "type": "hotel", 
        "id": 1
    }

tuples = []
def unfold(my_dict, prefix = ''):
    global tuples
    if prefix:
        prefix += '_'
    for k, v in my_dict.items():
        if not isinstance(v, dict):
                tuples.append((prefix+k,v))
        else:
            for k2, v2 in v.items():
                unfold(v2,prefix=prefix+k+'_'+k2)

unfold(hotel)
import json
print json.dumps(dict(tuples), indent=4)



