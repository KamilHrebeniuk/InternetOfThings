from flask import Flask, render_template, Response
from flask_restful import Resource, Api
from datetime import datetime, timedelta
from random import randrange
import csv

app = Flask(__name__)
api = Api(app)

# Open csv timezones database
with open('timezones.csv', newline='') as f:
    reader = csv.reader(f)
    timeData = list(reader)


# Check if country_id is on a country list
def get_country(country_id):
    counter = 1
    while country_id != timeData[counter - 1][0] and counter < len(timeData):
        counter += 1

    return counter


# Response as HTML site
class Country(Resource):
    def get(self, country_id):
        counter = get_country(country_id)

        if counter == len(timeData):
            return "Can't find"
        else:
            now = datetime.now()
            now += timedelta(seconds=int(timeData[counter - 1][1]) - 7200)
            current_time = now.strftime("%H:%M")
            target = "Current time in " + timeData[counter - 1][0]
            time = current_time
            return Response((render_template("index.html", rand=randrange(5), target=target, time=time)),
                            mimetype='text/html')


api.add_resource(Country, '/<country_id>')

if __name__ == '__main__':
    app.run(port='5002')
