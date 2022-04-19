import json
import random
import time

from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
# generate device ID with pub prefix randomly
_client_id = 'pub_server_1'

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


def publish(client, topic, json_name_file):
    msg_count = 0
    with open(f'configs/{json_name_file}', 'r') as filehand:
        dict = json.loads(filehand.read())
    data = json.dumps(dict)
    result = client.publish(topic, data)
    status = result[0]
    if status == 0:
        print(f"Send to topic `{topic}` `{data}` ")
    else:
        print(f"Failed to send message to topic {topic}")
    msg_count += 1


def run(topic, json_name_file):
    client = connect_mqtt()
    client.loop_start()
    publish(client, topic, json_name_file)
    client.loop_stop()


if __name__ == '__main__':
    run()
