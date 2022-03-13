import server.pub_server


def menu():
    print("Выберите пункт меню")
    print("1. Первичный запрос кода устройства ")
    print("2. Запрос текущего состояния об устройстве ")
    print("3. Запрос информации об устройстве ")
    print("4. Отправка команды на устройство ")
    print("5. Выход ")
    point_menu = int(input("Введите пункт меню: "))
    while point_menu != 5:
        match (point_menu):
            case 2:
                server.pub_server.run("CMD_10001", "GET_DEVICE_INFO")
            case 3:
                server.pub_server.run("CMD_10001", "GET_STATE_NOW")
        print("Выберите пункт меню")
        print("1. Первичный запрос кода устройства ")
        print("2. Запрос текущего состояния об устройстве ")
        print("3. Запрос информации об устройстве ")
        print("4. Отправка команды на устройство ")
        print("5. Выход ")
        point_menu = int(input("Введите пункт меню: "))

if __name__ == '__main__':
    menu()