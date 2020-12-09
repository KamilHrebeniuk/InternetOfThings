import json

import paho.mqtt.client as mqtt
import time
import sys
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

clients = [
    {"broker": "mqtt.eclipse.org", "port": 1883, "name": "blank", "sub_topic": "Power1", "pub_topic": "Power1"},
    {"broker": "mqtt.eclipse.org", "port": 1883, "name": "blank", "sub_topic": "Power2", "pub_topic": "Power2"},
    {"broker": "mqtt.eclipse.org", "port": 1883, "name": "blank", "sub_topic": "Power3", "pub_topic": "Power3"},
    {"broker": "mqtt.eclipse.org", "port": 1883, "name": "blank", "sub_topic": "Power4", "pub_topic": "Power4"},
    {"broker": "mqtt.eclipse.org", "port": 1883, "name": "blank", "sub_topic": "Power5", "pub_topic": "Power5"},
    {"broker": "mqtt.eclipse.org", "port": 1883, "name": "blank", "sub_topic": "Power6", "pub_topic": "Power6"},
    {"broker": "mqtt.eclipse.org", "port": 1883, "name": "blank", "sub_topic": "Power7", "pub_topic": "Power7"},
    {"broker": "mqtt.eclipse.org", "port": 1883, "name": "blank", "sub_topic": "Power8", "pub_topic": "Power8"},
]
clients_amount = len(clients)

out_queue = []


# Write response to file with a timestamp as a name
class listenHTTP(Resource):
    def post(self):
        out_queue.append(json.loads(request.get_json()))

        if len(out_queue) == int(sys.argv[2]):
            average_power = 0
            average_voltage = 0
            queue_length = len(out_queue)
            for x in range(queue_length):
                average_power += out_queue[x]["power"]
                average_voltage += out_queue[x]["voltage"]
            print("Average power consumption: " + str(average_power / queue_length) + "W")
            print("Average voltage available: " + str(average_voltage / queue_length * 230) + "V")


def on_message(client, userdata, message):
    time.sleep(1)
    out_queue.append(json.loads(str(message.payload.decode("utf-8"))))


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        for i in range(clients_amount):
            if clients[i]["client"] == client:
                topic = clients[i]["sub_topic"]
                break

        client.subscribe(topic)
    else:
        print("Bad connection Returned code=", rc)
        client.loop_stop()


def Create_connections():
    for i in range(clients_amount):
        cname = "client" + str(i)
        t = int(time.time())
        client_id = cname + str(t)
        client = mqtt.Client(client_id)
        clients[i]["client"] = client
        clients[i]["client_id"] = client_id
        clients[i]["cname"] = cname
        broker = clients[i]["broker"]
        port = clients[i]["port"]
        client.connect(broker, port)

        client.on_connect = on_connect
        client.on_message = on_message
        client.loop_start()
        while not client.connected_flag:
            time.sleep(0.05)


def listenMQTT():
    mqtt.Client.connected_flag = False

    Create_connections()

    print("All clients connected ")
    time.sleep(5)

    while 1:
        time.sleep(10)
        queue_length = len(out_queue)
        print("Queue length ", queue_length)
        average_power = 0
        average_voltage = 0
        for x in range(queue_length):
            average_power += out_queue[x]["power"]
            average_voltage += out_queue[x]["voltage"]
        print("Average power consumption: " + str(average_power / queue_length) + "W")
        print("Average voltage available: " + str(average_voltage / queue_length * 230) + "V")


if __name__ == '__main__':
    if sys.argv[1] == 'HTTP':
        api.add_resource(listenHTTP, '/')
        app.run(port='5004')
    elif sys.argv[1] == 'MQTT':
        listenMQTT()
    else:
        print("Protocol not found")
