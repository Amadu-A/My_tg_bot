import sqlite3


def processing_user_db(people_id):
    # если id есть в БД sqlite, то работаем с имеющимся
    # если id нет в БД sqlite, то создаем
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER,
        count_hotels INT,
        city TEXT,
        destinationId INT,
        sorting TEXT,
        priceMin INT,
        priceMax INT,
        landmarkIds REAL,
        check_in TEXT,
        check_out TEXT,
        command TEXT,
        currency TEXT,
        locale TEXT);
    """)
    connect.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
       order_id INT PRIMARY KEY,
       user_id INTEGER,
       date TEXT,
       command TEXT,
       cite TEXT,
       data TEXT);
    """)
    connect.commit()

    cursor.execute(f"SELECT user_id FROM users WHERE user_id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        user_id = [people_id]
        cursor.execute("INSERT INTO users(user_id) VALUES(?);", user_id)
        connect.commit()
    # удаление
    # people_id = message.chat.id
    # cursor.execute(f'DELETE FROM login_id WHERE id = {people_id}')
    # connect.commit()

def adding_values_db(people_id, value, param):
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = {people_id}")
    # cursor.execute(f"INSERT INTO users({param}) VALUES(\"{value}\");")
    cursor.execute(f"UPDATE users SET {param} = \"{value}\" WHERE user_id = {people_id}")
    # cursor.execute(f"INSERT INTO users({param}) VALUES(f'{value}');") тоже ошибка
    connect.commit()

def get_user_table_db(people_id):
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_id = {people_id}")
    one_result = cursor.fetchone()
    return one_result

def get_maxorder_db(id: int) -> int:
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM orders WHERE user_id = {id}")
    one_result = cursor.fetchall()
    if len(one_result):
        print(len(one_result), one_result)
        one_result = max(one_result, key = lambda x: x[0])[0]
        return one_result
    else:
        return 0

def get_data_order_db(id: int): # TODO если пусто, то будет ошибка
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM orders WHERE user_id = {id} ORDER BY order_id")
    lst = cursor.fetchall()
    if len(lst) > 0:
        return lst
    else:
        return [('', '', '', 'История пуста')]

def get_order_table_db(id):
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM orders WHERE user_id = {id}")
    one_result = cursor.fetchall()
    return one_result

def adding_orders_db(id_order, id_user, date, command, cite, value):
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute("""INSERT INTO orders(order_id, user_id, date, command, cite, data)
    VALUES(?, ?, ?, ?, ?, ?);""", (id_order, id_user, date, command, cite, value))
    connect.commit()
