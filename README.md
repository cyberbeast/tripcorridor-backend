To hydrate the Database with fake data, run
```
$ cd Hydration/bin
$ ./buil-address-hierarchy.sh
$ ./add-hotels.sh
```
This method of hydration is a quick and dirty way.
Will be modified in future.

To start the server, run
```
$ ./bin/start-server.sh
```
This restart the **Neo4j Database** and **Flask Server**.

To call the Natural Query API, use the details below 
and make a **POST** call as shown below.

API details | Value | Comment
------------|-------|--------
user name | "TripCorridor" | 
key | "NjQwNzlkNmI1MWI5YWI3YjVjODM0Yjc2YzFkN2I4YjNlMWI5YmMyYw==" | Generated using base64
port | 5544 | Don't use 6000 any more
method | POST |
ip address | 0.0.0.0 | Or consult your web admin


```
$ curl -i \ 
        -u TripCorridor:NjQwNzlkNmI1MWI5YWI3YjVjODM0Yjc2YzFkN2I4YjNlMWI5YmMyYw==, \
        -X POST -H "Content-Type: application/json"  \
        -d '{"wit_ai_response": <your response from wit.ai> }' \
        http://localhost:5544/api/naturalquery/execute
```
