# python3.6
import json
import device.pub_device

from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
username = 'emqx'
password = 'public'


def connect_mqtt(client_id) -> mqtt_client:
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


def subscribe(client: mqtt_client, topics, directory):
    def on_message(client, userdata, msg):
        dictionary = json.loads(msg.payload.decode())
        if dictionary['type'] == 'GET_DEVICE_INFO':
            device.pub_device.run('DEVICE__INFO', directory + '/DEVICE__INFO')
        if dictionary['type'] == 'GET_STATE_NOW':
            device.pub_device.run('STATE__RESPONSE', directory + '/STATE__RESPONSE')
        if dictionary['type'] == 'CMD':
            device.pub_device.run('CMD__RESPONSE', directory + '/CMD__RESPONSE')
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    for topic in topics:
        client.subscribe(topic)

    client.on_message = on_message


def run(topics, client_id, directory):
    client = connect_mqtt(client_id)
    subscribe(client, topics, directory)
    client.loop_forever()

