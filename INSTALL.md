*To install neo4j, run*

```
$ cd backend
$ ./bin/install-neo4j.sh
```
*To start the server, run *

```
$ sudo /var/lib/neo4j/bin/neo4j restart
```

or 

```
$ sudo service neo4j-serive restart
```

To hydrate the server, modify the file

```
$ cd RandomDataHydration
$ vi hydrate_everything.py
```

change line 15, authentication() as required
and the script

```
$ python hydrate_everything.py
```

wait for about 2 minutes for server to hydrate

*To run the flask app, in settings.py file modify*

1. NEO4J_DB_URL_PORT = "localhost:7474"
2. NEO4J_DB_USERNAME = "neo4j"
3. NEO4J_DB_PASSWORD = "Tr!pC0rr!d0r"

Maybe you can have a localtunnel as 
```
$ lt -s neo4jdb -p 7474
```

then replace "localhost:7474" to "neo4jdb.localtunnel.me",
in settings.py

Then run the flask app as,
```
$ python api.py &
```


