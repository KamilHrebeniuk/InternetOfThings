import json
import random
import sys
import time
import paho.mqtt.client as mqtt

import requests
from flask import Flask, jsonify
from flask_restful import Resource, Api
from datetime import datetime, timedelta
import csv

appPure = Flask(__name__)
apiPure = Api(appPure)

# Open csv timezones database
with open(sys.argv[4], newline='') as f:
    reader = csv.reader(f, delimiter=';')
    data = list(reader)


def simulate():
    if sys.argv[1] == 'HTTP':
        while 1:
            time.sleep(random.randint(int(sys.argv[2]), int(sys.argv[3])))
            sendHTTP(toJSON())
    elif sys.argv[1] == 'MQTT':
        client = mqtt.Client("P1")
        client.connect(sys.argv[5], 1883, 60)
        while 1:
            time.sleep(random.randint(int(sys.argv[2]), int(sys.argv[3])))
            sendMQTT(client, toJSON())
    else:
        print("Protocol not found")


def toJSON():
    rand_row = random.randint(0, len(data))
    data_set = {
        "address": data[rand_row][0],
        "direction": data[rand_row][1],
        "registration": data[rand_row][2]
    }

    json_data = json.dumps(data_set)
    return json_data


def sendHTTP(json_data):
    print(json_data)
    return requests.post(sys.argv[5], json=json_data)


def sendMQTT(client, json_data):
    print(json_data)
    client.publish(sys.argv[6], json_data)


# 1. Protocol
# 2. Min delay
# 3. Max delay
# 4. Source
# 5. IP
# 6. Topic
if __name__ == '__main__':
    random.seed(time)
    simulate()

