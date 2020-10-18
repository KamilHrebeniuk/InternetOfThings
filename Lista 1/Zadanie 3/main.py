import sys
import paho.mqtt.client as mqtt
import requests
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)


# Action when response is received
def on_message(client, userdata, message):
    print("Watching for: ", message.topic)
    print("Current time: ", str(message.payload.decode("utf-8")))
    data = {
        "students": 000000,
        "received_target": message.topic,
        "received_time": str(message.payload.decode("utf-8"))
    }
    return requests.post('http://localhost:5003', json=data)


if __name__ == '__main__':
    client = mqtt.Client("P2")
    client.on_message = on_message
    client.connect("mqtt.eclipse.org", 1883, 60)
    client.subscribe(sys.argv[1])
    client.loop_forever(1)
