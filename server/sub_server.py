# python3.6

import json
import pub_server
import psycopg2
import device.db.state_response
import device.db.device_info
import device.db.device_authorisation
import device.db.telemetry

from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topics = ["urg_GET__CODE", "urg_hello", "urg_DEVICE__INFO", "urg_STATE__RESPONSE", "urg_CMD__RESPONSE", "urg_TELEMETRY"]
# generate device ID with pub prefix randomly
client_id = 'urg_sub_server_'
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
        print()
        print(f"Received from `{data.topic}` topic `{data.payload.decode()}`")
        dictionary = json.loads(data.payload.decode())
        if data.topic == 'urg_hello':
            # Проверка есть ли устройство в системе, есть ли нет, то зарегать его и дать ему id TODO: Я это не сделал
            result_code = device.db.device_authorisation.check_registration(dictionary['code'])
            if result_code != 0:
                device.db.device_authorisation.db_device_authorisation(result_code, 1)
                pub_server.run(f"urg_CMD_{dictionary['code']}", f"REPLY_AUTHORISATION_{dictionary['code']}")
            else:
                print("Устройство не зарегестрировано в системе")

        if data.topic == "urg_DEVICE__INFO":
            device.db.device_info.db_device_info(dictionary)


        if data.topic == "urg_STATE__RESPONSE":
            device.db.state_response.db_state_response(dictionary)


        if data.topic == "urg_TELEMETRY":
            device.db.telemetry.db_telemetry(dictionary)


    for topic in topics:
        client.subscribe(topic)
    client.on_message = on_message


def check_authorisation(code):
    import device.db.config_connection
    name_table = 'authorisation_devices'
    sql_code = f'''SELECT device_id FROM {name_table} WHERE code='{code}' '''
    cur = device.db.config_connection.con.cursor()
    cur.execute(sql_code)
    result = cur.fetchall()

    device.db.config_connection.con.commit()
    device.db.config_connection.con.close()

    if result == "":
        return 0
    return result


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
