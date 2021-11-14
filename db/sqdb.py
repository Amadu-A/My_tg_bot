import sqlite3


def processing_user_db(people_id):
    # если id есть в БД sqlite, то работаем с имеющимся инстансом User
    # если id нет в БД sqlite, то создаем инстанс User
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
        best TEXT,
        currency TEXT,
        locale TEXT);
    """)
    connect.commit()

    #people_id = message.chat.id
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
    #people_id = message.chat.id
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = {people_id}")
    # cursor.execute(f"INSERT INTO users({param}) VALUES(\"{value}\");")
    cursor.execute(f"UPDATE users SET {param} = \"{value}\" WHERE user_id = {people_id}")
    # cursor.execute(f"INSERT INTO users({param}) VALUES(f'{value}');") тоже ошибка
    connect.commit()

def get_user_table_db(people_id):
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    #people_id = message.chat.id
    cursor.execute(f"SELECT * FROM users WHERE user_id = {people_id}")
    one_result = cursor.fetchone()
    return one_result