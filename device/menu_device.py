from pathlib import *
import json
import device.pub_device
import device.db.device_authorisation


def menu(code, directory):

    dir = Path.cwd().parent
    with open(f'{dir}/server/configs/REPLY_AUTHORISATION_WITH_WIFI_{code}', 'r') as filehand:
        dict = json.loads(filehand.read())
    data = json.dumps(dict)
    device_id = json.loads(data)['data']['id']

    print("Выберите пункт меню")
    print("1. Авторизация ")
    print("2. Отправка данных телеметрии ")
    print("3. Выход ")
    point_menu = try_parse_int((input("Введите пункт меню: ")))
    while point_menu is None or point_menu < 1 or point_menu > 3:
        point_menu = try_parse_int((input("Введите корретный пункт меню: ")))
    while True:
        match (point_menu):
            case 1:
                if not check_authoristaion(code):
                    device.pub_device.run("urg_hello", f"{directory}/CODE")
                else:
                    print('Накопитель уже авторизован в системе')
            case 2:
                if check_authoristaion(code):
                    device.pub_device.run(f"urg_TELEMETRY", f"{directory}/TELEMETRY")
                else:
                    print('Error! Накопитель не авторизован в системе')
            case 3:
                exit(code, device_id)
                break

        print("Выберите пункт меню")
        print("1. Авторизация ")
        print("2. Отправка данных телеметрии ")
        print("3. Выход ")
        point_menu = try_parse_int((input("Введите пункт меню: ")))
        while point_menu is None or point_menu < 1 or point_menu > 3:
            point_menu = try_parse_int((input("Введите корретный пункт меню: ")))


def try_parse_int(s, base = 10, val = None):
    try:
        return int(s, base)
    except:
        return val


def check_authoristaion(code):
    list_devices = device.db.device_authorisation.get_open_devices()
    for list_code in list_devices:
        if str(list_code) == str(code):
            return True
    return False


def exit(code, device_id):
    if check_authoristaion(code):
        device.db.device_authorisation.db_device_authorisation(device_id, 0)
