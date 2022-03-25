from datetime import datetime

import psycopg2
import device.db.config_connection

name_table = 'state_devices'


class DeviceState:
    def __init__(self, device_id, cmd, state, info):
        self.device_id = device_id
        self.cmd = cmd
        self.state = state
        self.info = info
        self.time = datetime.now()


def db_state_response(dictionary):
    con = psycopg2.connect(
        database=device.db.config_connection.database,
        user=device.db.config_connection.user,
        password=device.db.config_connection.password,
        host=device.db.config_connection.host,
        port=device.db.config_connection.port
    )

    devices_info = json_state_response(dictionary)
    cur = con.cursor()
    for device_info in devices_info:
        sql_code = f'''INSERT INTO {name_table} (device_id, cmd, state, info, time) 
        VALUES ('{device_info.device_id}', '{device_info.cmd}', '{device_info.state}', 
        '{device_info.info}', '{device_info.time}')'''
        cur.execute(sql_code)
    con.commit()
    print('Информация о состоянии устройства добавлена в базе данных')
    con.close()


def json_state_response(dictionary):
    device_id = dictionary['deviceId']
    states_arr = dictionary['state']
    devices_state = list()
    for state_arr in states_arr:
        cmd = state_arr['cmd']
        state = state_arr['state']
        info = state_arr['info']
        devices_state.append(DeviceState(device_id, cmd, state, info))
    return devices_state
