import sqlite3

import telebot
from telebot import types
# import logging
# import re
# import json
#
#
from config import BOT_TOKEN
# import botrequests
from botrequests.high_lowprice import *
from botrequests.settings import get_list_locale


bot = telebot.TeleBot(BOT_TOKEN)


# query_param = {
#         'count_hotels': None,
#         'city': None,
#         'sorting': 'PRICE',
#         'locale': 'en_US',
#         'destinationId': None
# }
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

@bot.message_handler(commands=['lowprice', 'highprice'])
def welcome(message):
    processing_user_db(message)
    param = get_user_table_db(message)
    print(param)
    print(param[-1])
    if str(get_user_table_db(message)[-1]).isdigit():
        value = 'en_US'
        adding_values_db(message, value, param='locale')

    query_param = {
        'count_hotels': None,
        'city': None,
        'sorting': None,
        'destinationId': None,
        'locale': value
    }
    if message.text == 'lowprice':
        query_param['sorting'] = 'PRICE'
    elif message.text == 'highprice':
        query_param['sorting'] = 'PRICE'
    bot.send_message(message.chat.id, 'Введите город')
    city = message.text
    city = city.title()
    print(message.text)
    print(query_param)
    bot.register_next_step_handler(message, callback=keyboard_city, query_param=query_param)


# @bot.message_handler(commands=['highprice'])
# def welcome(message):
#     bot.send_message(message.chat.id, 'Команда highprice в стадии разработки')

@bot.message_handler(commands=['bestdeal'])
def welcome(message):
    bot.send_message(message.chat.id, 'Команда bestdeal в стадии разработки')

@bot.message_handler(commands=['history'])
def welcome(message):
    bot.send_message(message.chat.id, 'Команда history в стадии разработки')

@bot.message_handler(content_types=['text'])
def get_textmessages(message):
    processing_user_db(message)
    bot.send_message(message.from_user.id, text=help_msg)


def get_city_count(message):

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
        if elem['name'].lower() == city:
            new_btn = types.InlineKeyboardButton(text=elem['name'] + ',' + elem['caption'].split(',')[-1],
                                                callback_data=elem['destinationId'],
                                                 parse_mode='html')
            kb_cities.add(new_btn)
    if len(kb_cities.to_dict()['inline_keyboard']) == 0:
        # логер
        msg = bot.send_message(chat_id, f'Ошибка! Город{city} не найден. Попробуйте еще раз.')
        bot.register_next_step_handler(msg, keyboard_city)
    else:
        bot.send_message(message.from_user.id, reply_markup=kb_cities,
                                       text='Выберите подходящий город:', parse_mode='html')

        #query_param['destinationId'] = prev_msg.text
        #print(query_param)
        #bot.register_next_step_handler(message=prev_msg, callback=get_city_count, query_param=query_param)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if len(call.data) == 5 and call.data[2] == '_':
        language = call.data
        #query_param = call.query_param
        print(language)
        #print(query_param)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вы выбрали язык {language}', reply_markup=None)
        processing_user_db(call.message)
        adding_values_db(call.message, language, param='locale')
        #query_param['locale'] = language
        #print(query_param)
    elif len(str(call.data)) < 3:
        count_hotels = call.data
        print(count_hotels)
        #query_param = call.query_param
        #print(query_param)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Идет поиск отелей', reply_markup=None)
        adding_values_db(call.message, count_hotels, param='count_hotels')
        query_param_tuple = get_user_table_db(call.message)
        query_param = {
            'count_hotels': query_param_tuple[1],
            'city': query_param_tuple[2],
            'sorting': query_param_tuple[3],
            'locale': query_param_tuple[4],
            'destinationId': query_param_tuple[5]
        }

        query_param['count_hotels'] = count_hotels
        print(query_param)
        for hotel in get_hotels(query_param): # TODO не хватает аргумента city_id
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
        index = int(call.data)
        print(index)
        processing_user_db(call.message)
        adding_values_db(call.message, index, param='destinationId')
        # set_user_info('city_name', data[index]['name'], chat_id)
        # set_user_info('city_id', data[index]['destinationId'], chat_id)
        # логер
        #print(call.query_param)
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
    cursor.execute(f"INSERT INTO users({param}) VALUES({value});")
    # cursor.execute(f"INSERT INTO users({param}) VALUES(f'{value}');") тоже ошибка
    connect.commit()

def get_user_table_db(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    people_id = message.chat.id
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = {people_id}")
    one_result = cursor.fetchone()
    return one_result




if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)