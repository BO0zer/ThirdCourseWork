# python 3.6
import json
import random
import time

from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
_topic = ["GET__CODE"]
# generate device ID with pub prefix randomly
_client_id = f'python-mqtt-{10001}'

username = 'emqx'
password = 'public'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(_client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, topic):
    msg_count = 0
    msg = {"code": "10001"}
    data = json.dumps(msg)
    result = client.publish(_topic[0], data)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{data}` to topic `{_topic[0]}`")
    else:
        print(f"Failed to send message to topic {_topic[0]}")
    msg_count += 1



def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()

if __name__ == '__main__':
    run()
