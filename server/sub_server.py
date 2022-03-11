# python3.6

import random
import json
import pub_server

from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = ["GET__CODE", "hello_1"]
# generate device ID with pub prefix randomly
client_id = 'real'
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
        if(data.topic == 'hello_1'):
            print("ура")
            pub_server.run()
        print(f"Received `{data.payload.decode()}` from `{data.topic}` topic")
    client.subscribe(topic[0])
    client.subscribe(topic[1])
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

def menu():
    print("Выберите пункт меню")
    print("1. Первичный запрос кода устройства ")
    print("2. Запрос текущего состояния об устройстве ")
    print("3. Запрос информации об устройстве ")
    print("4. Отправка команды на устройство ")
    print("5. Выход ")

if __name__ == '__main__':
    run()