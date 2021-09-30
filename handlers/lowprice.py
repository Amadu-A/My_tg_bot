from telebot import types
from main import bot


# @bot.message_handler(content_types=['text'])
# def get_textmessages(message):
#     if message.text == "Привет":
#         bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#     elif message.text == "/hello-world":
#         bot.send_message(message.from_user.id, "Напишите: привет")
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /hello-world")