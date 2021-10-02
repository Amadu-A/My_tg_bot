import random

import telebot
from telebot import types
# import logging
# import re
# import requests
# import json
#
#
from config import BOT_TOKEN, API_KEY
import botrequests


bot = telebot.TeleBot(BOT_TOKEN)
headers = {
        'x-rapidapi-host': 'hotels4.p.rapidapi.com',
        'x-rapidapi-key': API_KEY
    }
my_url = 'https://hotels4.p.rapidapi.com/locations/search'

help_msg = '/lowprice - самые дешёвые отели\n' \
           '/highprice - самые дорогие отели в городе\n' \
           '/bestdeal - отели, подходящие по цене и удаленности от центра\n' \
           '/history - история поиска'

@bot.message_handler(content_types=['text'])
def get_textmessages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/hello-world":
        bot.send_message(message.from_user.id, "Напишите: привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /hello-world")


bot.polling(none_stop=True, interval=0)