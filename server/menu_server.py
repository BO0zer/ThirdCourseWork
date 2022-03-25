import server.pub_server
import device.db.config_connection
import psycopg2


def get_open_devices():
    con = psycopg2.connect(
        database=device.db.config_connection.database,
        user=device.db.config_connection.user,
        password=device.db.config_connection.password,
        host=device.db.config_connection.host,
        port=device.db.config_connection.port
    )
    cur = con.cursor()
    sql_code = f'''SELECT code from 
    (SELECT authorisation_devices.device_id, MIN(authorisation_devices.device_id), devices.code from public.authorisation_devices
    INNER JOIN devices 
        ON (authorisation_devices.device_id = devices.device_id)
        GROUP BY authorisation_devices.device_id, devices.code
        HAVING MIN(authorisation_devices.state_auth) > 0 ) AS something'''


    cur.execute(sql_code)

    con.commit()
    results = cur.fetchall()
    con.close()


    list_devices = list()
    for result in results:
        list_devices.append(result[0])

    return list_devices


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
            case 1:
                server.pub_server.run("GET_DEVICE_CODE", "GET_DEVICE_CODE")
            case 2:
                list_devices_code = get_open_devices()
                i = 1
                for code in list_devices_code:
                    print(f"{i}. {code}")
                    i+=1
                print(f"{i}. Выход")
                point_extra_menu = int(input("Введите номер накопителя: "))
                if point_extra_menu != i:
                    server.pub_server.run(f"urg_CMD_{code}", "GET_STATE_NOW")

            case 3:
                list_devices_code = get_open_devices()
                i = 1
                for code in list_devices_code:
                    print(f"{i}. {code}")
                    i+=1
                print(f"{i}. Выход")
                point_extra_menu = int(input("Введите номер накопителя: "))
                if point_extra_menu != i:
                    server.pub_server.run(f"urg_CMD_{code}", "GET_DEVICE_INFO")
            case 4:
                list_devices_code = get_open_devices()
                i = 1
                for code in list_devices_code:
                    print(f"{i}. {code}")
                    i += 1
                print(f"{i}. Выход")
                point_extra_menu = int(input("Введите номер накопителя: "))
                if point_extra_menu != i:
                    server.pub_server.run(f"urg_CMD_{code}", "CMD")

        print("Выберите пункт меню")
        print("1. Первичный запрос кода устройства ")
        print("2. Запрос текущего состояния об устройстве ")
        print("3. Запрос информации об устройстве ")
        print("4. Отправка команды на устройство ")
        print("5. Выход ")
        point_menu = int(input("Введите пункт меню: "))

if __name__ == '__main__':
    menu()
