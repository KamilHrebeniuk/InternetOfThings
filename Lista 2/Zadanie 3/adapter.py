import paho.mqtt.client as mqtt
import time
import sys
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

clients = [
    {"broker": "mqtt.eclipse.org", "port": 1883, "name": "blank", "sub_topic": "Place", "pub_topic": "Place"},
    {"broker": "mqtt.eclipse.org", "port": 1883, "name": "blank", "sub_topic": "Power", "pub_topic": "Power"},
    {"broker": "mqtt.eclipse.org", "port": 1883, "name": "blank", "sub_topic": "Beach", "pub_topic": "Beach"},
    {"broker": "mqtt.eclipse.org", "port": 1883, "name": "blank", "sub_topic": "Bicycle", "pub_topic": "Bicycle"},
    {"broker": "mqtt.eclipse.org", "port": 1883, "name": "blank", "sub_topic": "Buildings", "pub_topic": "Buildings"}
]
clients_amount = len(clients)

out_queue = []


# Write response to file with a timestamp as a name
class listenHTTP(Resource):
    def post(self):
        out_queue.append(request.get_json())

        if len(out_queue) == sys.argv[2]:
            summary_length = 0
            for x in range(len(out_queue)):
                summary_length += (len(out_queue[len(out_queue) - 1]))
                print(out_queue.pop())
            print("Summary length ", summary_length)


def on_message(client, userdata, message):
    time.sleep(1)
    out_queue.append(str(message.payload.decode("utf-8")))


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
        print("Queue length ", len(out_queue))
        summary_length = 0
        for x in range(len(out_queue)):
            summary_length += (len(out_queue[len(out_queue) - 1]))
            print(out_queue.pop())
        print("Summary length ", summary_length)


if __name__ == '__main__':
    if sys.argv[1] == 'HTTP':
        api.add_resource(listenHTTP, '/')
        app.run(port='5004')
    elif sys.argv[1] == 'MQTT':
        listenMQTT()
    else:
        print("Protocol not found")
