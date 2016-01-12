from py2neo import authenticate, watch, Graph
import config

class Neo4jDatabase:
    """
        This class queries the neo4j graph Neo4jDatabase
        and returns the formatted response.

        The response is json object of the form
        {
            "query": "a valid cypher query string that was input",
            "status" : "success or failed, a string",
            "results" : [resultObject],
            "count": <int: length of results list>
        }

        where resultObject has the structure that depends on the 
        RETURN values in the cypher query.

        Example: 

        If the cypher query has a return statement as 
        RETURN x,y,z
        then the result object has the form
        
        {
            "x":{xObj},
            "y":{yObj},
            "z":{zObj}
        }

        This object is row in neo4j database as 

         x   |  y   |  z
        -----+------+-----
        xObj | yObj | zObj

        If no result is found in the database then we get
        a response in the form
        {
            "query": "a cypher query",
            "status": "failed",
            "results": [],
            "count": 0
        }

    """
    def __init__(self):
        authenticate(config.NEO4J_DB_URL_PORT,
            config.NEO4J_DB_USERNAME,
            config.NEO4J_DB_PASSWORD)
        watch('httpstream')
        watch('py2neo.cypher')
        self.graph = Graph()

    def execute(self,query):
        results = self.graph.cypher.execute(query)
        response = self._format_response(results)
        response['query'] = query
        if results:
            response['status'] = "success"
        else:
            response['status'] = "failed"
        
        return response

    def _format_response(self,results):
        response = {'results':[]}
        if len(results) > 0:
            for result in results:
                headers = [x for x in dir(result) if not x.startswith('_')]
                result_json = {}
                for header in headers:
                    result_json[header] = getattr(result,header).properties
                response['results'].append(result_json)

        response['count'] = len(results)
        return response