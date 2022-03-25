from pathlib import *
import json
import device.pub_device
import device.db.device_authorisation

def menu(code, directory):
    print("Выберите пункт меню")
    print("1. Авторизация ")
    print("2. Отправка данных телеметрии ")
    print("3. Выход ")
    point_menu = int(input("Введите пункт меню: "))
    while True:
        match (point_menu):
            case 1:
                device.pub_device.run("urg_hello", f"{directory}/CODE")
            case 2:
                device.pub_device.run("urg_DEVICE__DATA", f"{directory}/TELEMETRY")
            case 3:
                dir = Path.cwd().parent
                with open(f'{dir}/server/configs/REPLY_AUTHORISATION_{code}', 'r') as filehand:
                    dict = json.loads(filehand.read())
                data = json.dumps(dict)
                device_id = json.loads(data)['data']['id']
                device.db.device_authorisation.db_device_authorisation(device_id, 0)
                print("Все гуд")
                break

        print("Выберите пункт меню")
        print("1. Авторизация ")
        print("2. Отправка данных телеметрии ")
        print("3. Выход ")
        point_menu = int(input("Введите пункт меню: "))
