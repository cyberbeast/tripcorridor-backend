
class CypherQueryGenerator:
    """
        This Object generates the Cypher query to read only
        From the attribute of Selector and Filter object
    """
    def generate(self,selector,filter):
        """
            The lonely method that generate the cypher query
        """
        query = ""
    
        if selector.intent == "to list":
            if selector.what == "hotels":
                query = """
                MATCH (hotel:Hotel)
                WHERE hotel.address =~ ".*%s.*"
                RETURN hotel
                LIMIT 5
                """ % selector.where
            elif selector.what == "points of interest in major destination":
                query = """
                MATCH (poi:PointOfInterest)<-[:HAS]-(md:MajorDestination)
                WHERE md.name = "%s"
                RETURN poi
                LIMIT 5
                """ % selector.where
            elif selector.what == "points of interest in state":
                query = """
                MATCH (poi:PointOfInterest)<-[:HAS]-(s:State)
                WHERE s.name = "%s"
                RETURN poi
                LIMIT 5
                """ % selector.where

        return query
