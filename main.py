import sqlite3
import telebot
from telebot import types
# import logging
# import re

from config import BOT_TOKEN
from botrequests.high_lowprice import *
from botrequests.settings import get_list_locale
from botrequests.bestdeal import get_best_hotels


bot = telebot.TeleBot(BOT_TOKEN, parse_mode='html')
help_msg = '/lowprice - самые дешёвые отели\n' \
           '/highprice - самые дорогие отели в городе\n' \
           '/bestdeal - отели, подходящие по цене и удаленности от центра\n' \
           '/history - история поиска'


@bot.message_handler(commands=['command1'])
def language(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for elem in get_list_locale():
        item = types.InlineKeyboardButton(elem['name'], callback_data=elem['hcomLocale'])
        markup.add(item)
    bot.send_message(message.from_user.id , text='Выберите язык', reply_markup=markup)

# @bot.message_handler(commands=['command2'])
# def language(message):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     for elem in get_list_currency():
#         item = types.InlineKeyboardButton(elem['name'], callback_data=elem['hcomLocale'])
#         markup.add(item)
#     bot.send_message(message.from_user.id , text='Выберите валюту', reply_markup=markup)

@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def welcome(message):
    processing_user_db(message)
    value = get_user_table_db(message)
    print(value)
    print(value[-1])
    cur_value = value[-2]
    value = value[-1]
    if str(get_user_table_db(message)[-1]).isdigit() or get_user_table_db(message)[-1] is None:
        value = 'en_US'
        adding_values_db(message, value, param='locale')
    if get_user_table_db(message)[-2] is None:
        cur_value = 'USD'
        adding_values_db(message, cur_value, param='currency')

    query_param = {
        'count_hotels': None,
        'city': None,
        'sorting': None,
        'destinationId': None,
        'best': None,
        'currency': cur_value,
        'locale': value
    }
    print('Команда', message.text)
    adding_values_db(message, value='no', param='best')
    if message.text == '/lowprice':
        query_param['sorting'] = 'PRICE'
    elif message.text == '/highprice':
        query_param['sorting'] = 'PRICE_HIGHEST_FIRST'
    elif message.text == '/bestdeal':
        query_param['sorting'] = 'PRICE'
        adding_values_db(message, value='yes', param='best')
    adding_values_db(message, query_param['sorting'], param='sorting')
    bot.send_message(message.chat.id, 'Введите город')
    city = message.text
    city = city.title()
    print(message.text)
    print(query_param)
    bot.register_next_step_handler(message, callback=keyboard_city, query_param=query_param)

@bot.message_handler(commands=['history'])
def welcome(message):
    bot.send_message(message.chat.id, 'Команда history в стадии разработки')

@bot.message_handler(content_types=['text'])
def get_textmessages(message):
    processing_user_db(message)
    bot.send_message(message.from_user.id, text=help_msg)

def keyboard_city(message, query_param):
    """Клавиатура с вариантами городов"""
    chat_id = message.chat.id
    print(chat_id)
    city = message.text.lower()
    print(city)
    print(query_param)
    data = get_city_list(city, query_param)
    print(data)
    kb_cities = types.InlineKeyboardMarkup(row_width=1)
    for elem in data:
        #if city.lower() in elem['name'].lower():
        new_btn = types.InlineKeyboardButton(text=elem['name'] + ',' + elem['caption'].split(',')[-1],
                                                callback_data=f"{elem['destinationId']}+{elem['name']}",
                                                parse_mode='html')
        kb_cities.add(new_btn)
    if len(kb_cities.to_dict()['inline_keyboard']) == 0:
        # логер
        msg = bot.send_message(chat_id, f'Ошибка! Город{city} не найден. Попробуйте еще раз.')
        bot.register_next_step_handler(message=msg, callback=keyboard_city, query_param=query_param)
    else:
        bot.send_message(message.from_user.id, reply_markup=kb_cities,
                                       text='Выберите подходящий город или район:', parse_mode='html')

def get_city_count(message):

    # if get_user_table_db(message)[-3] == 'yes':
    #     print(get_user_table_db(message)[-3])
    #     bot.send_message(message.chat.id, 'Введите ценовой диапазон (например: 100-2000)')
    #     bot.register_next_step_handler(message, callback=get_size_price)
    #     try:
    #         result = message.text.split('-')
    #         priceMin = min(int(result[0]), int(result[1]))
    #         priceMax = max(int(result[0]), int(result[1]))
    #         if priceMin < 0 or priceMax <= 0:
    #             raise Exception
    #         adding_values_db(message, priceMin, param='priceMin')
    #         adding_values_db(message, priceMax, param='priceMax')
    #         bot.send_message(message.chat.id, 'Введите допустимую удаленность от центра города в метрах')
    #         if int(message.text) < 0:
    #             raise Exception
    #         landmarkIds = round(int(message.text) / 1000 / 1.6093, 1)
    #         adding_values_db(message, landmarkIds, param='landmarkIds')
    #     except (TypeError, IndexError, Exception):
    #         get_city_count(message)


        #bot.register_next_step_handler(message, callback=get_size_price)

    # клавиатура
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # item1 = types.KeyboardButton('5')
    # item2 = types.KeyboardButton('10')
    # markup.add(item1, item2)
    print('id города', message.text)
    # print(query_param)
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('5', callback_data='5')
    item2 = types.InlineKeyboardButton('10', callback_data='10')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Выберите количество отелей', reply_markup=markup)

def get_size_price(message):
    print(get_user_table_db(message)[-3])
    bot.send_message(message.chat.id, 'Введите ценовой диапазон (например: 100-2000)')
    print(message.text.split('-'))
    try:
        result = message.text.split('-')
        priceMin = min(int(result[0]), int(result[1]))
        priceMax = max(int(result[0]), int(result[1]))
        if priceMin < 0 or priceMax <= 0:
            raise Exception
        adding_values_db(message, priceMin, param='priceMin')
        adding_values_db(message, priceMax, param='priceMax')
        bot.register_next_step_handler(message, callback=get_distance)
    except (TypeError, IndexError, Exception):
        get_size_price(message)
    bot.register_next_step_handler(message, callback=get_distance)

def get_distance(message):
    try:
        bot.send_message(message.chat.id, 'Введите допустимую удаленность от центра города в метрах')
        if int(message.text) < 0:
            raise Exception
        landmarkIds = round(int(message.text) / 1000 / 1.6093, 1)
        adding_values_db(message, landmarkIds, param='landmarkIds')
        bot.register_next_step_handler(message, callback=get_city_count)
    except (TypeError, IndexError, Exception):
        get_distance(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if len(call.data) == 5 and call.data[2] == '_':
        language = call.data
        print(language)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вы выбрали язык {language}', reply_markup=None)
        processing_user_db(call.message)
        adding_values_db(call.message, language, param='locale')
    elif len(str(call.data)) < 3:
        count_hotels = call.data
        print(count_hotels)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Идет поиск отелей', reply_markup=None)
        adding_values_db(call.message, count_hotels, param='count_hotels')
        query_param_tuple = get_user_table_db(call.message)
        print(query_param_tuple)
        query_param = {
            'count_hotels': query_param_tuple[1],
            'city': query_param_tuple[2],
            'destinationId': query_param_tuple[3],
            'sorting': query_param_tuple[4],
            'priceMin': query_param_tuple[6],
            'priceMax': query_param_tuple[7],
            'landmarkIds': query_param_tuple[8],
            'currency': query_param_tuple[9],
            'locale': query_param_tuple[10]
        }

        query_param['count_hotels'] = count_hotels
        print(query_param)
        if get_user_table_db(call.message)[-3] == 'no':
            for hotel in get_hotels(query_param):
                print(hotel)
                print(hotel.get_hotel())
                bot.send_message(chat_id=call.message.chat.id, text=hotel.get_hotel())
        elif get_user_table_db(call.message)[-3] == 'yes':
            for hotel in get_best_hotels(query_param):
                print(hotel)
                print(hotel.get_hotel())
                bot.send_message(chat_id=call.message.chat.id, text=hotel.get_hotel())
    else: # str(call.data).isalpha():
        print('='*10)
        #query_param = call.query_param
        print(call.data)
        chat_id = int(call.message.chat.id)
        print(chat_id)
        bot.delete_message(chat_id, call.message.message_id)
        #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Выберите количество отелей', reply_markup=None)
        value = call.data.split('+')
        print(value)
        processing_user_db(call.message)
        adding_values_db(call.message, value[0], param='destinationId')
        adding_values_db(call.message, value[1], param='city')
        # логер
        #print(call.query_param)
        if get_user_table_db(call.message)[-3] == 'yes':
            get_size_price(call.message)
        else:
            get_city_count(call.message)
        #print(call.message)
        #bot.register_next_step_handler(call.message, callback=get_city_count)

def processing_user_db(message):
    # если id есть в БД sqlite, то работаем с имеющимся инстансом User
    # если id нет в БД sqlite, то создаем инстанс User
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER,
        count_hotels INT,
        city TEXT,
        destinationId INT,
        sorting TEXT,
        priceMin INT,
        priceMax INT,
        landmarkIds INT,
        best TEXT,
        currency TEXT,
        locale TEXT);
    """)
    connect.commit()

    people_id = message.chat.id
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        user_id = [message.chat.id]
        cursor.execute("INSERT INTO users(user_id) VALUES(?);", user_id)
        connect.commit()
    # удаление
    # people_id = message.chat.id
    # cursor.execute(f'DELETE FROM login_id WHERE id = {people_id}')
    # connect.commit()

def adding_values_db(message, value, param):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    people_id = message.chat.id
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = {people_id}")
    # cursor.execute(f"INSERT INTO users({param}) VALUES(\"{value}\");")
    cursor.execute(f"UPDATE users SET {param} = \"{value}\" WHERE user_id = {people_id}")
    # cursor.execute(f"INSERT INTO users({param}) VALUES(f'{value}');") тоже ошибка
    connect.commit()

def get_user_table_db(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    people_id = message.chat.id
    cursor.execute(f"SELECT * FROM users WHERE user_id = {people_id}")
    one_result = cursor.fetchone()
    return one_result




if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)