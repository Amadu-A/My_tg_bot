import requests
import telebot
from telebot import types

from main import bot, headers



my_url = 'https://hotels4.p.rapidapi.com/locations/search'
my_url2 = 'https://hotels4.p.rapidapi.com/properties/list'
url_lang = 'https://hotels4.p.rapidapi.com/get-meta-data'
params = {'query': 'new york', 'locale': 'en_US'}


def get_city(message):
    city = message.text
    city = city.title()
    bot.send_message(message.chat.id, 'Введите количество отелей')
    bot.register_next_step_handler(message, get_count_hotels)
    print(city)
    #return city

def get_count_hotels(message):
    # переделаю через инлайнклавиатуру. Сделаю кнопками (меньше ошибок, меньше условий)
    count_hotels = bot.send_message(message.chat.id, 'Введите количество отелей')
    print(count_hotels)
    #return count_hotels

def search_hotels(message):
    # city = message.text
    # city = city.title()
    # bot.send_message(message.chat.id, 'Введите количество отелей')
    # bot.register_next_step_handler(message, get_count_hotels)
    # print(city)
    pass

# @bot.message_handler(content_types=['text'])
# def get_textmessages(message):
#     if message.text == "Привет":
#         bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#     elif message.text == "/hello-world":
#         bot.send_message(message.from_user.id, "Напишите: привет")
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /hello-world")