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

To call the Natural Query API,
use the *API_USERNAME: "TripCorridor"*
and *API_KEY: "NjQwNzlkNmI1MWI5YWI3YjVjODM0Yjc2YzFkN2I4YjNlMWI5YmMyYw=="*
and make a **POST** call as shown below.

```
$ curl -i \ 
        -u $API_USERNAME:$API_KEY, \
        -H "Content-Type: application/json" \
        -X POST \
        -d '{"wit_ai_response": <your response from wit.ai> }' \
        http://localhost:5544/api/naturalquery/execute
```
