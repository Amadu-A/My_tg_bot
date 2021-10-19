import sqlite3
import datetime
import telebot
from telebot import types
# import logging
# import re
# import json
#
#
from config import BOT_TOKEN, API_KEY
# import botrequests
from botrequests.lowprice import *
#from botrequests.lowprice import get_hotels


bot = telebot.TeleBot(BOT_TOKEN)
headers = {
        'x-rapidapi-host': 'hotels4.p.rapidapi.com',
        'x-rapidapi-key': API_KEY
    }
url_id_city = 'https://hotels4.p.rapidapi.com/locations/search'
url_detail = 'https://hotels4.p.rapidapi.com/properties/list'
url_lang = 'https://hotels4.p.rapidapi.com/get-meta-data'
params = {'query': 'new york', 'locale': 'en_US'}
date_today = datetime.datetime.today().strftime('%Y-%m-%d')
date_tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')


query_param = {
        'count_hotels': None,
        'city': None,
        'sorting': 'PRICE'
}

help_msg = '/lowprice - самые дешёвые отели\n' \
           '/highprice - самые дорогие отели в городе\n' \
           '/bestdeal - отели, подходящие по цене и удаленности от центра\n' \
           '/history - история поиска'


@bot.message_handler(commands=['lowprice'])
def welcome(message):
    # выбираем язык. Будет скрипт-меню с кнопкой
    language = 'ru_RU'
    bot.send_message(message.chat.id, 'Введите город')
    # тут будет скрипт с библиотекой re, который будет искать похожие названия городов, если
    # не обнаружится совпадений
    city = message.text
    city = city.title()
    print(message.text)
    bot.register_next_step_handler(message, callback=get_city, query_param=query_param)


@bot.message_handler(commands=['highprice'])
def welcome(message):
    bot.send_message(message.chat.id, 'Команда highprice в стадии разработки')

@bot.message_handler(commands=['bestdeal'])
def welcome(message):
    bot.send_message(message.chat.id, 'Команда bestdeal в стадии разработки')

@bot.message_handler(commands=['history'])
def welcome(message):
    bot.send_message(message.chat.id, 'Команда history в стадии разработки')

@bot.message_handler(content_types=['text'])
def get_textmessages(message):
    bot.send_message(message.from_user.id, text=help_msg)

def get_city(message, query_param: dict):
    city = message.text
    print(city)
    city = city.title()

    query_param['city'] = city

    # клавиатура
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # item1 = types.KeyboardButton('5')
    # item2 = types.KeyboardButton('10')
    # markup.add(item1, item2)

    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('5', callback_data='5')
    item2 = types.InlineKeyboardButton('10', callback_data='10')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Выберите количество отелей', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    count_hotels = call.data
    print(count_hotels)
    print(query_param)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Идет поиск отелей', reply_markup=None)
    query_param['count_hotels'] = count_hotels
    print(query_param)
    for hotel in get_hotels(query_param):
        print(hotel)
        print(hotel.get_hotel())
        bot.send_message(chat_id=call.message.chat.id, text=hotel.get_hotel())


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)