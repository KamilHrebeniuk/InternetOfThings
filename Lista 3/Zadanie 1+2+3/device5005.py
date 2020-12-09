import threading
from concurrent.futures import thread

from flask import Flask, jsonify
from flask_cors import CORS
import json
import random
import sys
import time
import paho.mqtt.client as mqtt
from datetime import datetime

import requests
from flask import Flask, jsonify
from flask_restful import Api
import csv

app = Flask(__name__)
CORS(app)

appPure = Flask(__name__)
apiPure = Api(appPure)

state = 1           # 0 -> Turned Off || 1 -> Turned On
power = 50
power_real = 0

target = sys.argv[1]

def simulate():
    print ("Ready to simulate")
    while 1:
        if state == 1:
            time.sleep(random.randint(int(sys.argv[2]), int(sys.argv[3])))
            if target == 'HTTP':
                sendHTTP(toJSON())
            elif target == 'MQTT':
                client = mqtt.Client("P1")
                client.connect("mqtt.eclipse.org", 1883, 60)
                sendMQTT(client, toJSON())
            else:
                print("Protocol not found")


def toJSON():
    now = datetime.now()
    global power
    global power_real
    voltage = random.randint(210, 250) / 230
    power_real = power * voltage
    data_set = {
        "time": now.strftime("%H:%M:%S"),
        "power": power_real,
        "voltage": voltage
    }

    json_data = json.dumps(data_set)
    return json_data


def sendHTTP(json_data):
    print(json_data)
    print("HTTP!")
    return requests.post("http://localhost:5004", json=json_data)


def sendMQTT(client, json_data):
    print(json_data)
    print("MQTT!")
    client.publish(sys.argv[6], json_data)

def mainDevice():
    random.seed(time)
    simulate()

def controller():
    app.run(port=sys.argv[4])

if __name__ == '__main__':
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        return jsonify('{"name":"' + sys.argv[5] + '", "status":"Working", "communication":"' + target + '"}')

    @app.route('/state-change', methods=['GET', 'POST'])
    def state_change():
        global state
        if state == 0:
            state = 1
            return jsonify('{"state":"Turned On"}')
        else:
            state = 0
            return jsonify('{"state":"Turned Off"}')

    @app.route('/communication', methods=['GET', 'POST'])
    def communication_change():
        global target
        if target == "MQTT":
            target = "HTTP"
            return jsonify('{"communication":"HTTP"}')
        else:
            target = "MQTT"
            return jsonify('{"communication":"MQTT"}')

    @app.route('/power-up', methods=['GET', 'POST'])
    def power_up():
        global power
        if power <= 190:
            power += 10
        return jsonify('{"power":"' + str(power) + '"}')

    @app.route('/power-down', methods=['GET', 'POST'])
    def power_down():
        global power
        if power >= 10:
            power -= 10
        return jsonify('{"power":"' + str(power) + '"}')

    @app.route('/status', methods=['GET', 'POST'])
    def status():
        if state == 0:
            return jsonify('{"status":"Ready"}')
        else:
            return jsonify('{"status":"Working", "power":"' + str(power_real) + '", "communication":"' + target + '"}')

    try:
        threading.Thread(target=mainDevice).start()
        threading.Thread(target=controller).start()
    except:
        print("Error: unable to start thread")





