import json
import random
import sqlite3

import requests
import telebot
from telebot import types
# import logging
# import re
# import json
#
#
from config import BOT_TOKEN, API_KEY
#import botrequests
# from botrequests.lowprice import get_city, search_hotels


bot = telebot.TeleBot(BOT_TOKEN)
headers = {
        'x-rapidapi-host': 'hotels4.p.rapidapi.com',
        'x-rapidapi-key': API_KEY
    }
my_url = 'https://hotels4.p.rapidapi.com/locations/search'
url_lang = 'https://hotels4.p.rapidapi.com/get-meta-data'
params = {'query': 'new york', 'locale': 'en_US'}
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
    bot.register_next_step_handler(message, get_city)
    bot.send_message(message.chat.id, 'Идет поиск отелей')

    #bot.register_next_step_handler(message, search_hotels)


    # location_dict = requests.get(my_url, headers=headers, params=params)
    # response_langu = requests.request("GET", url_lang, headers=headers)



    # with open('test.json', 'w') as file:
    #     json.dump(json.loads(location_dict.text), file, indent=4)
    # print(response_langu.text)
    # with open('lang.json', 'w') as file:
    #     json.dump(json.loads(response_langu.text), file, indent=4)


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

def get_city(message):
    city = message.text
    print(city)
    city = city.title()
    bot.send_message(message.chat.id, 'Введите количество отелей')
    bot.register_next_step_handler(message, get_count_hotels)
    print(city)
    #return city

def get_count_hotels(message):
    pass

bot.polling(none_stop=True, interval=0)