import json
from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Country(Resource):
    def post(self):
        f = open("output/" + datetime.now().strftime("%H-%M-%S") + ".json", "w")
        f.write(json.dumps(request.get_json()))
        f.close()


api.add_resource(Country, '/')

if __name__ == '__main__':
    app.run(port='5003')
