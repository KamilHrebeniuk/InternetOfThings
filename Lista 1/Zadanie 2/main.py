import json
import paho.mqtt.client as mqtt
import time
import requests
from flask import Flask
import sys

app = Flask(__name__)


# Set place to watch
def get_data(target):
    return requests.get('http://localhost:5001/' + target).content


# Action when response is received
def on_message(client, userdata, message):
    print("Watching for: ", message.topic)
    print("Current time: ", str(message.payload.decode("utf-8")))


if __name__ == '__main__':
    client = mqtt.Client("P1")
    client.on_message = on_message
    client.connect("mqtt.eclipse.org", 1883, 60)
    client.loop_start()

    while 1:
        responseContent = json.loads(get_data(sys.argv[1]))
        client.subscribe(responseContent["target"])
        client.publish(responseContent["target"], responseContent["time"])
        time.sleep(5)


