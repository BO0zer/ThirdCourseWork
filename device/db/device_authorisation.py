from datetime import datetime

import psycopg2
import device.db.config_connection

name_table_auth = 'authorisation_devices'
name_table_reg = 'devices'


class DeviceAuth:
    def __init__(self, device_id, state_auth):
        self.device_id = device_id
        self.state_auth = state_auth
        self.time = datetime.now()


def db_device_authorisation(device_id, state_auth):
    con = psycopg2.connect(
        database=device.db.config_connection.database,
        user=device.db.config_connection.user,
        password=device.db.config_connection.password,
        host=device.db.config_connection.host,
        port=device.db.config_connection.port
    )

    device_authorisation = DeviceAuth(device_id, state_auth)
    cur = con.cursor()

    # 1 - накопитель вошел в систему, 0 - выходит из нее
    if state_auth == 1:
        sql_code_delete = f'''DELETE FROM {name_table_auth} WHERE device_id = '{device_authorisation.device_id}' '''
        cur.execute(sql_code_delete)

    sql_code_insert = f'''INSERT INTO {name_table_auth} (device_id, state_auth, time) 
    VALUES ('{device_authorisation.device_id}', '{device_authorisation.state_auth}', '{device_authorisation.time}')'''

    cur.execute(sql_code_insert)

    con.commit()
    print('Накопитель авторизован')
    con.close()


def check_authorisation(code):
    con = psycopg2.connect(
        database=device.db.config_connection.database,
        user=device.db.config_connection.user,
        password=device.db.config_connection.password,
        host=device.db.config_connection.host,
        port=device.db.config_connection.port
    )

    sql_code = f'''SELECT device_id FROM {name_table_reg} WHERE code='{code}' '''
    cur = con.cursor()
    cur.execute(sql_code)

    results = cur.fetchall()
    result = results[0]

    con.commit()
    con.close()

    if result[0] == "":
        return 0
    return result[0]