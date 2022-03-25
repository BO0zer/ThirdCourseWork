import psycopg2
import device.db.config_connection

name_table = 'info_about_devices'


class DeviceInfo:
    def __init__(self, device_id, sn, pin, hw, sw, mode, ap,
                 ac_chg_start, ac_chg_end, autonomy_start, autonomy_end):
        self.device_id = device_id
        self.sn = sn
        self.pin = pin
        self.hw = hw
        self.sw = sw
        self.mode = mode
        self.ap = ap
        self.ac_chg_start = ac_chg_start
        self.ac_chg_end = ac_chg_end
        self.autonomy_start = autonomy_start
        self.autonomy_end = autonomy_end


def db_device_info(dictionary):
    con = psycopg2.connect(
        database=device.db.config_connection.database,
        user=device.db.config_connection.user,
        password=device.db.config_connection.password,
        host=device.db.config_connection.host,
        port=device.db.config_connection.port
    )

    device_info = json_device_info(dictionary)
    sql_code = f'''INSERT INTO {name_table} (device_id, sn, pin, hw, sw, mode, ap, 
    ac_chg_start, ac_chg_end, autonomy_start, autonomy_end) 
    VALUES ('{device_info.device_id}', '{device_info.sn}', '{device_info.pin}', '{device_info.hw}'
    , '{device_info.sw}', '{device_info.mode}', {device_info.ap}
    , '{device_info.ac_chg_start}', '{device_info.ac_chg_end}'
    , '{device_info.autonomy_start}', '{device_info.autonomy_end}')'''

    cur = con.cursor()
    cur.execute(sql_code)

    con.commit()
    print('Информация о накопителе добавлена в базу данных')
    con.close()


def json_device_info(dictionary):
    device_id = dictionary['deviceId']
    info = dictionary['info']

    sn = info['sn']
    pin = info['pin']
    hw = info['hw']
    sw = info['sw']
    mode = info['mode']
    ap = info['ap']
    times = info['times']

    ac_chg = times['ac_chg']
    ac_chg_start = ac_chg['start']
    ac_chg_end = ac_chg['end']

    autonomy = times['autonomy']
    autonomy_start = autonomy['start']
    autonomy_end = autonomy['end']

    device_info = DeviceInfo(device_id, sn, pin, hw, sw, mode, ap,
                             ac_chg_start, ac_chg_end, autonomy_start, autonomy_end)
    return device_info

