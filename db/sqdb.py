import sqlite3
from typing import Union
from botrequests.settings import translate_google
from logging_module import *

@logger.catch
@logging_decorator
def processing_user_db(people_id: int) -> None:

    """
    Функция, создающая таблицы базы данных SQLite
    При добавлении колонок выполнить команду:
    ALTER TABLE languages ADD COLUMN <имя_колонки-bot_23> TEXT AFTER <имя_колонки-bot_22>;
    :param people_id: int
    :return: None
    """

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

    cursor.execute("""CREATE TABLE IF NOT EXISTS languages(
        language TEXT,
        command_1 TEXT,  command_2 TEXT,  command_3 TEXT,  command_4 TEXT,  command_5 TEXT,  command_6 TEXT, command_7 TEXT,
        bot_1 TEXT, bot_2 TEXT, bot_3 TEXT, bot_4 TEXT, bot_5 TEXT, bot_6 TEXT, bot_7 TEXT, bot_8 TEXT, bot_9 TEXT, 
        bot_10 TEXT, bot_11 TEXT, bot_12 TEXT, bot_13 TEXT, bot_14 TEXT, bot_15 TEXT, bot_16 TEXT, bot_17 TEXT,
        bot_18 TEXT, bot_19 TEXT, bot_20 TEXT, bot_21 TEXT, bot_22 TEXT,
        msg_1 TEXT, msg_2 TEXT,  msg_3 TEXT,  msg_4 TEXT,  msg_5 TEXT,  msg_6 TEXT);
    """)

    text_tpl = (
        'ru',

        'Самые дешёвые отели',
        'Самые дорогие отели в городе',
        'Отели, подходящие по цене и удаленности от центра',
        'История поиска',
        'Настройки',
        'Указанная в результатах поиска цена будет актуальна после авторизации пользователя на сайте,  ',
        'Очистить историю',

        'Дата и время: ',
        'Команда: ',
        'Посмотреть на сайте: ',
        'Выберите язык',
        'Выберите валюту',
        'Другой',
        'Введите город',
        'Ошибка! Город',
        'не найден. Попробуйте еще раз.',
        'Выберите подходящий город или район:',
        'Выберите количество отелей',
        'Введите ценовой диапазон (например: 100-2000)',
        'Введите допустимую удаленность от центра города в километрах или милях',
        'Показать фото?',
        'Сколько фото показать?',
        'Идет поиск отелей',
        'ВЫБЕРИТЕ',
        'Выберите дату заезда',
        'Дату из прошлого выбирать нельзя',
        'Выберите дату отъезда',
        'История пуста',
        'Отелей по вашему запросу не найдено',

        'Рейтинг',
        'Цена за выбранный период за 1 человека',
        'Индекс',
        'Адрес',
        'от центра города',
        'Сайт'
    )

    cursor.execute(f"SELECT language FROM languages WHERE language = 'ru'")
    data = cursor.fetchone()
    if data is None:
        cursor.execute("""INSERT INTO languages(language,
                command_1,  command_2,  command_3,  command_4,  command_5,  command_6, command_7,
                bot_1, bot_2, bot_3, bot_4, bot_5, bot_6, bot_7, bot_8, bot_9, bot_10, bot_11, bot_12, bot_13, bot_14,
                bot_15, bot_16, bot_17, bot_18, bot_19, bot_20, bot_21, bot_22,
                msg_1, msg_2,  msg_3,  msg_4,  msg_5,  msg_6
                )
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                       text_tpl)
        connect.commit()

    cursor.execute(f"SELECT user_id FROM users WHERE user_id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        user_id = [people_id]
        cursor.execute("INSERT INTO users(user_id) VALUES(?);", user_id)
        connect.commit()

@logger.catch
@logging_decorator
def clear_history(id: int) -> None:
    """Удаляет историю из таблицы oders по id пользователя"""
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute(f'DELETE FROM orders WHERE user_id = {id}')
    connect.commit()

@logger.catch
@logging_decorator
def adding_user_id_db(id: int) -> None:
    """Функция добавляет id нового пользователя в таблицу users"""
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = {id}")
    data = cursor.fetchone()
    if data is None:
        user_id = [id]
        cursor.execute("INSERT INTO users(user_id) VALUES(?);", user_id)
        connect.commit()

@logger.catch
@logging_decorator
def adding_values_db(people_id: int, value: Union[int, float, str, None], param: str) -> None:
    """Функция добавляет значение по id пользователя в таблицу users"""
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = {people_id}")
    cursor.execute(f"UPDATE users SET {param} = \"{value}\" WHERE user_id = {people_id}")
    connect.commit()

@logger.catch
@logging_decorator_responce
def get_user_table_db(people_id: int) -> list:
    """Функция возвращает список кортежа по id пользователя из таблицы users"""
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_id = {people_id}")
    one_result = cursor.fetchone()
    return one_result

@logger.catch
@logging_decorator_responce
def get_maxorder_db(id: int) -> int:
    """Функция возвращает последний номер записи по id пользователя из таблицы orders"""
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM orders")    #  WHERE user_id = {id}
    one_result = cursor.fetchall()
    if len(one_result):
        one_result = max(one_result, key = lambda x: x[0])[0]
        return one_result
    else:
        return 0

@logger.catch
@logging_decorator_responce
def get_data_order_db(id: int) -> list:
    """Функция возвращает список из таблицы orders для истории поиска"""
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM orders WHERE user_id = {id} ORDER BY order_id")
    lst = cursor.fetchall()
    if len(lst) > 0:
        return lst
    else:
        return [('', '', '', 'История пуста')]

@logger.catch
@logging_decorator_responce
def get_order_table_db(id: int) -> list:
    """Функция возвращает список из таблицы orders"""
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM orders WHERE user_id = {id}")
    one_result = cursor.fetchall()
    return one_result

@logger.catch
@logging_decorator
def adding_orders_db(id_order: int, id_user: int, date: str, command: str, cite: str, value: str) -> None:
    """Функция добавляет данные в таблицу orders"""
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute("""INSERT INTO orders(order_id, user_id, date, command, cite, data)
    VALUES(?, ?, ?, ?, ?, ?);""", (id_order, id_user, date, command, cite, value))
    connect.commit()

@logger.catch
@logging_decorator
def adding_language_into_languages_db(param: str) -> None:
    """Функция добавляет язык в таблицу languages"""
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT language FROM languages WHERE language = '{param}'")
    data = cursor.fetchone()
    if data is None:
        cursor.execute("INSERT INTO languages(language) VALUES(?);", [param])
        connect.commit()

@logger.catch
@logging_decorator_responce
def get_translated_item_db(id, language: str, param: str) -> str:
    """Функция возвращает переведенное значение из таблицы languages, либо переводит его и добавляет в таблицу languages"""
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT \"{param}\" FROM languages WHERE language = \"{language}\"")
    one_result = cursor.fetchone()[0]
    if one_result is None:
        one_result = translate_google(text=get_rus_text(param), dest_google=language)
        if one_result != get_rus_text(param):
            cursor.execute(f"UPDATE languages SET \"{param}\" = \"{one_result}\" WHERE language = \"{language}\"")
            connect.commit()
        else:
            one_result = one_result[0]  # 'Выбранная локализация сегодня недоступна. ' +
            adding_values_db(id, value='ru_RU', param='locale')
    return one_result

@logger.catch
@logging_decorator_responce
def get_rus_text(param: str) -> str:
    """Функция возвращает русский текст, если локаль русская"""
    connect = sqlite3.connect('db\\users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT \"{param}\" FROM languages WHERE language = 'ru'")
    return cursor.fetchone()
