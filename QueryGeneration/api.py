from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from model import Model
import settings

app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()


model = Model(verbose = True)

@auth.get_password
def get_password(username):
    if username == settings.API_USERNAME:
        return settings.API_KEY
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)


class NaturalQueryAPI(Resource):
    """ 
        The Model object takes a natural language query,
        generates a Neo4j cypher query from its input,
        and returns the response after querying the 
        graph database.

        This class is a Flask app the provides a 
        an api endpoint at localhost:6000/api/naturalquery/execute
        with POST method. The data has to be json object of the 
        form {"query":"your natural language query string here"}

        Example:
        $cd your/server/path/here
        $python api.py

        In another terminal try
        $curl -i \ 
        -u mushtaque:secret \
        -H "Content-Type: application/json" \
        -X POST \
        -d '{"query": "Hotels in Bangalore"}' \
        http://localhost:6000/api/naturalquery/execute


    """ 
    decorators = [auth.login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('query', type=str, required=True,
                                location='json')
        super(NaturalQueryAPI, self).__init__()

    def post(self):
        """
            Extract the "query" value from the request
            that was posted and delegate the natural 
            query to the Model object

            Return the http response along with 200 OK
        """
        query = self.parser.parse_args()['query']
        response = model.execute(query)        
        return response,200
    
api.add_resource(NaturalQueryAPI, '/api/naturalquery/execute', endpoint='execute')

if __name__ == '__main__':
    app.run(debug=True,port = 6000)