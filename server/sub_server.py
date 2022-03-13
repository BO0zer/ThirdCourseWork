# python3.6

import random
import json
import pub_server
import pub_server

from paho.mqtt import client as mqtt_client

import server.pub_server

broker = 'broker.emqx.io'
port = 1883
topics = ["urg_GET__CODE", "urg_hello", "DEVICE__INFO", "STATE__RESPONSE", "CMD__RESPONSE"]
# generate device ID with pub prefix randomly
client_id = 'urg_sub_server'
username = 'emqx'
password = 'public'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        data = msg
        if data.topic == 'urg_hello':
            dictionary = json.loads(data.payload.decode())
            pub_server.run(f"CMD_{dictionary['code']}", 'REPLY_AUTHORISATION')
        print(f"Received `{data.payload.decode()}` from `{data.topic}` topic")
    for topic in topics:
        client.subscribe(topic)

    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
