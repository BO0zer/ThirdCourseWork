import device.pub_device


def menu(code, directory):
    print("Выберите пункт меню")
    print("1. Авторизация ")
    print("2. Отправка данных телеметрии ")
    print("3. Выход ")
    point_menu = int(input("Введите пункт меню: "))
    while point_menu != 5:
        match (point_menu):
            case 1:
                device.pub_device.run("urg_hello", f"{directory}/CODE_{code}")
        print("Выберите пункт меню")
        print("1. Авторизация ")
        print("2. Отправка данных телеметрии ")
        print("3. Выход ")
        point_menu = int(input("Введите пункт меню: "))
