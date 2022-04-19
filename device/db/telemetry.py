from datetime import datetime

import psycopg2
import device.db.config_connection

name_table = 'telemetry'


class Telemetry:
    def __init__(self, device_id, grid_volt, grid_freq, out_volt,
                 out_freq, out_app_pwr, out_load, batt_volt, batt_discharge,
                 batt_charging, batt_capacity, inv_tempr, mppt_tempr):
        self.device_id = device_id
        self.time = datetime.now()
        self.grid_volt = grid_volt
        self.grid_freq = grid_freq
        self.out_volt= out_volt
        self.out_freq = out_freq
        self.out_app_pwr = out_app_pwr
        self.out_load = out_load
        self.batt_volt = batt_volt
        self.batt_discharge = batt_discharge
        self.batt_charging = batt_charging
        self.batt_capacity = batt_capacity
        self.inv_tempr = inv_tempr
        self.mppt_tempr = mppt_tempr


def db_telemetry(dictionary):
    con = psycopg2.connect(
        database=device.db.config_connection.database,
        user=device.db.config_connection.user,
        password=device.db.config_connection.password,
        host=device.db.config_connection.host,
        port=device.db.config_connection.port
    )

    device_info = json_telemetry(dictionary)
    sql_code = f'''INSERT INTO {name_table} (device_id, time, grid_volt, grid_freq, out_volt, out_freq, out_app_pwr, 
    out_load, batt_volt, batt_discharge, batt_charging, batt_capacity, inv_tempr, mppt_tempr) 
    VALUES ('{device_info.device_id}', '{device_info.time}', {device_info.grid_volt}, {device_info.grid_freq}
    , {device_info.out_volt}, {device_info.out_freq}, {device_info.out_app_pwr}
    , {device_info.out_load}, {device_info.batt_volt}, {device_info.batt_discharge}
    , {device_info.batt_charging}, {device_info.batt_capacity}, {device_info.inv_tempr}, {device_info.mppt_tempr})'''

    cur = con.cursor()
    cur.execute(sql_code)

    con.commit()
    print('Телеметрия накопителя добавлена в базу данных')
    con.close()


def json_telemetry(dictionary):
    device_id = dictionary['deviceId']
    telemetry = dictionary['telemetry']

    grid_volt = telemetry['grid_volt']
    grid_freq = telemetry['grid_freq']
    out_volt = telemetry['out_volt']
    out_freq = telemetry['out_freq']
    out_app_pwr = telemetry['out_app_pwr']
    out_load = telemetry['out_load']
    batt_volt = telemetry['batt_volt']
    batt_discharge = telemetry['batt_discharge']
    batt_charging = telemetry['batt_charging']
    batt_capacity = telemetry['batt_capacity']
    inv_tempr = telemetry['inv_tempr']
    mppt_tempr = telemetry['mppt_tempr']

    device_info = Telemetry(device_id, grid_volt, grid_freq, out_volt, out_freq, out_app_pwr, out_load,
                            batt_volt, batt_discharge, batt_charging, batt_capacity, inv_tempr, mppt_tempr)
    return device_info

