import os
import pathlib
from pathlib import Path

# Константа, отвечающая за количество устройств накопителей
COUNT_DEVACES = 3


def menu():
    print("1. Выбрать устройство")
    print("2. Выйти")
    cmd = int(input())
    while cmd != 2:
        match cmd:
            case 1:
                print("Список доступных устройств:")
                for number in range(3):
                    print(number + 1, end=' ')
                print()
                device_number = input("Введите номер устройства: ")
                path = Path("configs_client", f"device_{device_number}")
# Нужно генерить скрипты pub для каждого устройства
# Запускать сервак

def main():
    menu()


if "__main__" == __name__:
    main()
