from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from model import Model
import settings, json, hashlib, base64
from model3 import Model3

app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()


model = Model3()
#Model2(verbose = True, fake_db_access = settings.FAKE_DB_ACCESS)
#model = Model(verbose = True)

@auth.get_password
def get_password(username):
    if username == settings.API_USERNAME:
        sha1_hash = hashlib.sha1(settings.API_USERNAME).hexdigest()
        return base64.b64encode(sha1_hash)
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
        an api endpoint at 0.0.0.0:5544/api/naturalquery/execute
        with POST method. The data has to be json object of the 
        form {"query":"your natural language query string here"}

        Example:
        $cd your/server/path/here
        $python api.py

        In another terminal try
        $curl -i \ 
        -u API_USERNAME:API_KEY, \
        -H "Content-Type: application/json" \
        -X POST \
        -d '{"wit_ai_response": <your response from wit.ai> }' \
        http://localhost:5544/api/naturalquery/execute


    """ 
    decorators = [auth.login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('wit_ai_response', type=dict, required=True,
            location='json')

        super(NaturalQueryAPI, self).__init__()

    def post(self):
        """
            Extract the "query" value from the request
            that was posted and delegate the natural 
            query to the Model object

            Return the http response along with 200 OK
        """
        parsed_args = self.parser.parse_args()
        response = model.execute(parsed_args)  
        return response,200
    
api.add_resource(NaturalQueryAPI, '/api/naturalquery/execute', endpoint='execute')

if __name__ == '__main__':
    app.run(debug=True,port = settings.API_PORT,
        host=settings.API_HOST_IP_ADDRESS)