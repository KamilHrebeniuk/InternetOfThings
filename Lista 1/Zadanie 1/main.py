from flask import Flask, jsonify
from flask_restful import Resource, Api
from datetime import datetime, timedelta
import csv

appPure = Flask(__name__)
apiPure = Api(appPure)

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


# Response as JSON
class CountryPure(Resource):
    def get(self, country_id):
        counter = get_country(country_id)

        if counter == len(timeData):
            return jsonify({
                "target": "Cant't find selected timezone",
                "time": "00:00:00"
            })
        else:
            now = datetime.now()
            now += timedelta(seconds=int(timeData[counter - 1][1]) - 7200)
            current_time = now.strftime("%H:%M:%S")
            target = timeData[counter - 1][0]
            time = current_time
            return jsonify({
                "target": target,
                "time": time
            })


apiPure.add_resource(CountryPure, '/<country_id>')

if __name__ == '__main__':
    appPure.run(port='5001')
