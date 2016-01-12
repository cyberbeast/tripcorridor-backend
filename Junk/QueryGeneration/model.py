from tagging import Tagger
from selecting import *
from filtering import *
from generating import CypherQueryGenerator

import json, requests
from database import Neo4jDatabase 


class Model:
    """
        The Model object takes a natural language query,
        generates a Neo4j cypher query from its input,
        and returns the response after querying the 
        graph database.
    """
    def __init__(self, verbose = False):
        """
            Build the Tagger, Selector, Filter
            CypherQueryGenerator and Neo4jDatabase object
        """

        self.verbose = verbose
        self.tagger = Tagger()
        self.selector = Selector()
        self.filter = None
        self.generator = CypherQueryGenerator()
        self.neo4jdb = Neo4jDatabase()

    def _generate_cypher_query(self):
        """
            Generate the cypher query using
            Selector,Filter and CypherQueryGenerator
            objects
        """

        return self.generator.generate(self.selector,self.filter)
        

    def _execute_cypher_query(self,query):
        """
            This is obsolete now
            It used to query the neo4j database
            by using another flask api running 
            at localhost:5000/api/cypher/execute
        """

        if not query:
            print "Cypher query is empty, cannot execute the query"
            return None
        neo4j_url = "http://localhost:5000/api/cypher/execute"
        data = json.dumps({'query': query})
        headers = {'content-type': 'application/json'} 
        r = requests.post(neo4j_url, data, auth=('neo4j', 'TRVLR'), headers=headers)
        return r.json()

    def _execute_cypher_query_directly(self,query):
        """
            This method delegates the query to Neo4jDatabase
            object
        """
        return self.neo4jdb.execute(query)

    def _print_formatted_response(self,response):
        """
            prints the response object in a pretty way
        """
        results = response['results']
        print """===========================================================
                            YOUR OUTPUT 
    ==========================================================="""
        if self.selector.what == 'hotels':
            print "Here is a list of hotels in %s" % self.selector.where
            for result in results:
                print """
            Name: %s
            Address: %s
            """ %  (result['hotel']['name'],result['hotel']['address'])  

        elif self.selector.what.startswith('points of interest'):
            print "Here are points of interest in %s" % self.selector.where
            for result in results:
                print """
            Name: %s
            Quick Info: %s
            """ % (result['poi']['name'],result['poi']['text'])          
        print "==========================================================="


    def execute(self,parsed_args):
        """
            This method has the main algorithm that
            turns the natural language query into 
            cypher query.

            The algorithm goes as follows

            1. Use Tagger object to tag and to apply 
                NER the natural query string
            2. Use Selector object to extract the
                selection information
            3. Use Filter object to extract 
                filtering information
            4. Generated the cypher query using 
                the data from Selector and Filter
                objects with CypherQueryGenerator
                object
            5. Use Neo4jDatabase objects to query 
                the neo4j graph database
            6. Return the response to the Flask app
                while will have Model object in it 

        """
        intent = parsed_args('intent')
        query = parsed_args['query']
        if self.verbose:
            print "query: ", query
        query = self.tagger.tag(query.lower())
        
        print "selector before applying...", self.selector
        self.selector.apply(query)
        if self.verbose:
            print self.selector
        
        neo4j_query = self._generate_cypher_query()
        if self.verbose:
            print "Generated Neo4j Cypher Query:"
            print neo4j_query
            print '-' * 80
        
            print "Executing Query..."
        response = self._execute_cypher_query_directly(neo4j_query)
        
        if self.verbose:
            print "Query response:"
            if response:
                print json.dumps(response, indent=4)
            else:
                print "None response returned"
            print '-' * 80
        
            self._print_formatted_response(response)
            print '-' * 80
        return response