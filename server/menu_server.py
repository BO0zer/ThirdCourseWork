import server.pub_server
import device.db.device_authorisation


def menu():
    print("Выберите пункт меню")
    print("1. Первичный запрос кода устройства ")
    print("2. Запрос текущего состояния об устройстве ")
    print("3. Запрос информации об устройстве ")
    print("4. Отправка команды на устройство ")
    print("5. Выход ")
    point_menu = try_parse_int((input("Введите пункт меню: ")))
    while point_menu is None or point_menu < 1 or point_menu > 5:
        point_menu = try_parse_int((input("Введите корретный пункт меню: ")))
    while point_menu != 5:
        match point_menu:
            case 1:
                server.pub_server.run("GET_DEVICE_CODE", "GET_DEVICE_CODE")
            case 2:
                list_devices_code = device.db.device_authorisation.get_open_devices()
                i = 1
                for code in list_devices_code:
                    print(f"{i}. {code}")
                    i+=1
                print(f"{i}. Выход")
                point_extra_menu = try_parse_int((input("Введите пункт меню: ")))
                while point_extra_menu is None or point_extra_menu < 1 or point_extra_menu > i:
                    point_extra_menu = try_parse_int((input("Введите корретный пункт меню: ")))
                if point_extra_menu != i:
                    server.pub_server.run(f"urg_CMD_{code}", "GET_STATE_NOW")

            case 3:
                list_devices_code = device.db.device_authorisation.get_open_devices()
                i = 1
                for code in list_devices_code:
                    print(f"{i}. {code}")
                    i+=1
                print(f"{i}. Выход")
                point_extra_menu = try_parse_int((input("Введите пункт меню: ")))
                while point_extra_menu is None or point_extra_menu < 1 or point_extra_menu > i:
                    point_extra_menu = try_parse_int((input("Введите корретный пункт меню: ")))
                if point_extra_menu != i:
                    server.pub_server.run(f"urg_CMD_{code}", "GET_DEVICE_INFO")
            case 4:
                list_devices_code = device.db.device_authorisation.get_open_devices()
                i = 1
                for code in list_devices_code:
                    print(f"{i}. {code}")
                    i += 1
                print(f"{i}. Выход")
                point_extra_menu = try_parse_int((input("Введите пункт меню: ")))
                print()
                while point_extra_menu is None or point_extra_menu < 1 or point_extra_menu > i:
                    point_extra_menu = try_parse_int((input("Введите корретный пункт меню: ")))
                if point_extra_menu != i:
                    server.pub_server.run(f"urg_CMD_{code}", "CMD")

        print()
        print("Выберите пункт меню")
        print("1. Первичный запрос кода устройства ")
        print("2. Запрос текущего состояния об устройстве ")
        print("3. Запрос информации об устройстве ")
        print("4. Отправка команды на устройство ")
        print("5. Выход ")
        point_menu = try_parse_int((input("Введите пункт меню: ")))
        while point_menu is None or point_menu < 1 or point_menu > 5:
            point_menu = try_parse_int((input("Введите корретный пункт меню: ")))


def try_parse_int(s, base = 10, val = None):
    try:
        return int(s, base)
    except:
        return val


if __name__ == '__main__':
    menu()
