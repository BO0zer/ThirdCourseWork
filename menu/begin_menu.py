import subprocess
import pathlib
import device.pub
import server.sub_server
from pathlib import Path


# Константа, отвечающая за количество устройств накопителей
COUNT_DEVACES = 3


def menu():
    print("1. Первичный запрос кода устройства")
    print("2. Запрос текущего состояния об устройстве")
    print("3. Запрос информации об устройстве")
    print("4. Отправка команд для устройств")
    print("5. Выход")
    cmd = int(input())
    while cmd != 6:
        match cmd:
            case 1:
                print("Список доступных устройств:")
                for number in range(COUNT_DEVACES):
                    print(number + 1, end=' ')
                print()
                device_number = input("Введите номер устройства: ")
                path = Path("configs_client", f"device_{device_number}")
                subprocess.run("python3 script1.py & python3 script2.py", shell=True)
                device.pub.run(f'python-mqtt-{10001}', "hello")
# Нужно генерить скрипты pub для каждого устройства
# Запускать сервак

def main():
    menu()


if "__main__" == __name__:
    main()
