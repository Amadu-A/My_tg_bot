import telebot
from telebot import types
from telebot.types import InputMediaPhoto
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import datetime as dt
# import logging
import re

from config import BOT_TOKEN, date_today, date_tomorrow
from botrequests.high_lowprice import get_city_list, get_hotels
from botrequests.settings import get_list_locale, translate_google, choose_currency
from botrequests.bestdeal import get_best_hotels
from db.sqdb import *
    #processing_user_db, adding_values_db, get_user_table_db, get_data_order_db, get_maxorder_db, adding_orders_db


bot = telebot.TeleBot(BOT_TOKEN, parse_mode='html')

@bot.message_handler(commands=['command1'])
def language(message: types.Message):
    """Инлайн-клавиатура для выбора языка и локали языка"""
    processing_user_db(message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    for key, val in get_list_locale().items():
        item = types.InlineKeyboardButton(key, callback_data=val)
        markup.add(item)
    text = translate_google('Выберите язык', message.chat.id)
    bot.send_message(message.from_user.id , text=text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: (len(call.data) == 5 and call.data[2] == '_'))
def callback_inline(call):
    """
    Хендлер для инлайн-клавиатуры. Отлавливает события в соответствии со значением callback_data:
    Выбор языка
    :param call: locale of the language
    """
    bot.delete_message(int(call.message.chat.id), call.message.message_id)
    #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text, reply_markup=None)
    if len(call.data) == 5 and call.data[2] == '_':
        language = call.data
        print(language)
        #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вы выбрали язык {language}', reply_markup=None)
    processing_user_db(call.message.chat.id)
    adding_values_db(call.message.chat.id, call.data, param='locale')

@bot.message_handler(commands=['command2'])
def currency(message: types.Message):
    processing_user_db(message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    for elem in choose_currency():
        item = types.InlineKeyboardButton(elem, callback_data=elem)
        markup.add(item)
    text = translate_google('Выберите валюту', message.chat.id)
    bot.send_message(message.from_user.id , text=text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: str(call.data) in choose_currency())
def callback_inline(call):
    """
    Хендлер для инлайн-клавиатуры. Отлавливает события в соответствии со значением callback_data:
    :param call: Выбор валюты
    """
    bot.delete_message(int(call.message.chat.id), call.message.message_id)
    processing_user_db(call.message.chat.id)
    adding_values_db(call.message.chat.id, str(call.data), param='currency')

@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def welcome(message: types.Message):
    """Функция, обрабатывающая команды '/lowprice', '/highprice', '/bestdeal'"""
    processing_user_db(message.chat.id)
    adding_values_db(message.chat.id, value=message.text, param='command')
    value = get_user_table_db(message.chat.id)
    print(value)
    print(value[-1])
    cur_value = value[-2]
    value = value[-1]
    if str(get_user_table_db(message.chat.id)[-1]).isdigit() or get_user_table_db(message.chat.id)[-1] is None:
        value = 'en_US'
        adding_values_db(message.chat.id, value, param='locale')
    if get_user_table_db(message.chat.id)[-2] is None:
        cur_value = 'USD'
        adding_values_db(message.chat.id, cur_value, param='currency')
    adding_values_db(message.chat.id, None, param='check_in')
    adding_values_db(message.chat.id, None, param='check_out')

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

    if message.text == '/lowprice':
        query_param['sorting'] = 'PRICE'
    elif message.text == '/highprice':
        query_param['sorting'] = 'PRICE_HIGHEST_FIRST'
    elif message.text == '/bestdeal':
        query_param['sorting'] = 'PRICE'   #'DISTANCE_FROM_LANDMARK'
        #adding_values_db(message.chat.id, value='yes', param='best')
    adding_values_db(message.chat.id, query_param['sorting'], param='sorting')
    text = translate_google('Введите город', message.chat.id)
    bot.send_message(message.chat.id, text)
    city = message.text
    city = city.title()
    print(message.text)
    print(query_param)
    bot.register_next_step_handler(message, callback=keyboard_city, query_param=query_param)

@bot.message_handler(commands=['history'])
def history(message: types.Message):
    """Функция, обрабатывающая команду '/history'"""
    print('что вернулось', get_data_order_db(message.chat.id))
    for request in get_data_order_db(message.chat.id):
        print(request)
        text = 'Дата и время: ' + request[-4] + '\n' + 'Команда: ' + request[-3] + '\n' + \
               'Посмотреть на сайте: ' + request[-2] + '\n' + request[-1]
        bot.send_message(chat_id=message.chat.id, text=text)

@bot.message_handler(content_types=['text'])
def get_textmessages(message: types.Message):
    """Функция, помогающая выбрать нужную команду для взаимодействия с ботом"""
    processing_user_db(message.chat.id)
    text1 = translate_google('самые дешёвые отели', message.chat.id)
    text2 = translate_google('самые дорогие отели в городе', message.chat.id)
    text3 = translate_google('отели, подходящие по цене и удаленности от центра', message.chat.id)
    text4 = translate_google('история поиска', message.chat.id)
    text5 = translate_google('Указанная в результатах поиска цена будет актуальна '
                             'после авторизации пользователя на сайте,  ', message.chat.id)
    help_msg = '/lowprice - {}\n/highprice - {}\n/bestdeal - {}\n/history - {}\n{} hotels.com'.format(
        text1, text2, text3, text4, text5)
    bot.send_message(message.from_user.id, text=help_msg)

def keyboard_city(message, query_param: dict):
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
        text = translate_google(f'Ошибка! Город{city} не найден. Попробуйте еще раз.', message.chat.id)
        msg = bot.send_message(chat_id, text)
        bot.register_next_step_handler(message=msg, callback=keyboard_city, query_param=query_param)
    else:
        text = translate_google('Выберите подходящий город или район:', message.chat.id)
        bot.send_message(message.from_user.id, reply_markup=kb_cities,
                                       text=text, parse_mode='html')

@bot.callback_query_handler(func=lambda call: '+' in str(call.data))
def callback_inline(call):
    """
    Хендлер для инлайн-клавиатуры. Отлавливает события в соответствии со значением callback_data:
    :param call: id отеля и имя города
    """
    bot.delete_message(int(call.message.chat.id), call.message.message_id)
    #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text, reply_markup=None)
    print('='*10)
    print(call.data)
    value = call.data.split('+')
    print(value)
    processing_user_db(call.message.chat.id)
    adding_values_db(call.message.chat.id, value[0], param='destinationId')
    adding_values_db(call.message.chat.id, value[1], param='city')
    bot.send_message(call.message.chat.id, 'Выберите дату заезда')
    check_in_out(call.message)

def get_city_count(message: types.Message):
    """Клавиатура с выбором количества отелей"""
    # клавиатура
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # item1 = types.KeyboardButton('5')
    # item2 = types.KeyboardButton('10')
    # markup.add(item1, item2)
    print('проверка 119 строка', message.text)
    # print(query_param)
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('5', callback_data='6')
    item2 = types.InlineKeyboardButton('10', callback_data='11')
    markup.add(item1, item2)
    text = translate_google('Выберите количество отелей', message.chat.id)
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: len(str(call.data)) < 3 and int(call.data) > 5)
def callback_inline(call):
    """
    Хендлер для инлайн-клавиатуры. Отлавливает события в соответствии со значением callback_data:
    Количество отелей
    :param call: count_hotels
    """
    bot.delete_message(int(call.message.chat.id), call.message.message_id)
    #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text, reply_markup=None)
    count_hotels = int(call.data) - 1
    print(count_hotels)
    adding_values_db(call.message.chat.id, count_hotels, param='count_hotels')
    print_photo(call.message)

def get_size_price(message: types.Message):
    """Функция для указания ценового диапазона в команде /bestdeal"""
    print(get_user_table_db(message.chat.id)[-3])
    text = translate_google('Введите ценовой диапазон (например: 100-2000)', message.chat.id)
    bot.send_message(message.chat.id, text)
    print(message.text.split('-'))
    bot.register_next_step_handler(message, callback=check_get_size_price)

def check_get_size_price(message: types.Message):
    """Функция для обработки ценового диапазона в команде /bestdeal"""
    try:
        result = re.findall(r'\d*', message.text)
        result = [int(size) for size in result if size.isdigit()]
        if len(result) != 2:
            raise Exception
        priceMin = min(int(result[0]), int(result[1]))
        priceMax = max(int(result[0]), int(result[1]))
        if priceMin < 0 or priceMax <= 0:
            raise Exception
        adding_values_db(message.chat.id, priceMin, param='priceMin')
        adding_values_db(message.chat.id, priceMax, param='priceMax')
        get_distance(message)
    except (TypeError, IndexError, Exception):
        get_size_price(message)

def get_distance(message: types.Message):
    """Функция для указания параметра удаленности в команде /bestdeal"""
    text = translate_google('Введите допустимую удаленность от центра города в метрах', message.chat.id)
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, callback=get_check_distance)

def get_check_distance(message: types.Message):
    """Функция для обработки параметра удаленности в команде /bestdeal"""
    try:
        landmarkIds = round(float(re.sub(r'[.,\s]', '.', message.text)), 2)
        adding_values_db(message.chat.id, landmarkIds, param='landmarkIds')
        get_city_count(message)
    except ValueError:
        get_distance(message)

def print_photo(message: types.Message):
    """Функция с клавиатурой выбора вывода фотографий отелей"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('✔', callback_data='yes')
    item2 = types.InlineKeyboardButton('✘', callback_data='none')
    markup.add(item1, item2)
    text = translate_google('Показать фото?', message.chat.id)
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: str(call.data) == 'yes')
def callback_inline(call):
    """
    Хендлер для инлайн-клавиатуры. Отлавливает события в соответствии со значением callback_data:
    :param call: Положительный ответ на вопрос о печати фото
    """
    bot.delete_message(int(call.message.chat.id), call.message.message_id)
    get_photos_count(call.message)

def get_photos_count(message: types.Message):
    """Функция с клавиатурой выбора количества фотографий отелей"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('1', callback_data=1)
    item2 = types.InlineKeyboardButton('3', callback_data=3)
    item3 = types.InlineKeyboardButton('5', callback_data=5)
    markup.add(item1, item2, item3)
    text = translate_google('Сколько фото показать?', message.chat.id)
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: str(call.data) == 'none' or
                                              (str(call.data).isdigit() and  len(call.data) == 1))
def callback_inline(call):
    """
    Хендлер для инлайн-клавиатуры. Отлавливает события в соответствии со значением callback_data
    :param call: Отрицательный ответ на печать фото, либо callback c количеством фото
    """
    bot.delete_message(int(call.message.chat.id), call.message.message_id)
    text = translate_google('Идет поиск отелей', call.message.chat.id)
    bot.send_message(chat_id=call.message.chat.id, text=text)
    query_param_tuple = get_user_table_db(call.message.chat.id)
    query_param = {
        'count_hotels': query_param_tuple[1],
        'city': query_param_tuple[2],
        'destinationId': query_param_tuple[3],
        'sorting': query_param_tuple[4],
        'priceMin': query_param_tuple[5],
        'priceMax': query_param_tuple[6],
        'landmarkIds': query_param_tuple[7],
        'check_in': query_param_tuple[8],
        'check_out': query_param_tuple[9],
        'currency': query_param_tuple[-2],
        'locale': query_param_tuple[-1],
        'user_id': call.message.chat.id
    }
    if str(call.data) == 'none':
        count_photos = 0
    else:
        count_photos = int(call.data)

    data = ''
    order_id = 1
    hotels_lst = []
    if get_user_table_db(call.message.chat.id)[-3] != '/bestdeal':
        hotels_lst = get_hotels(query_param, count_photos=count_photos)
    elif get_user_table_db(call.message.chat.id)[-3] == '/bestdeal':
        hotels_lst = get_best_hotels(query_param, count_photos=count_photos)
    for hotel in hotels_lst:
        bot.send_message(chat_id=call.message.chat.id, text=hotel.get_hotel())
        data += hotel.get_hotel() + '\n'
        if count_photos > 0:
            bot.send_media_group(chat_id=call.message.chat.id,
                             media=[InputMediaPhoto(media=path) for path in hotel.photo_path_list])
    if get_maxorder_db(call.message.chat.id) != None:
        order_id = get_maxorder_db(call.message.chat.id) + 1
    print(get_user_table_db(call.message.chat.id)[-3])
    adding_orders_db(id_order=order_id,
                     id_user=call.message.chat.id,
                     date=dt.datetime.now(),
                     command=get_user_table_db(call.message.chat.id)[-3],
                     cite=hotel.cite_for_db,
                     value=data)

def check_in_out(message: types.Message):
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)

@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):                                                              # TODO сравнение дат: чек ин и чек аут
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        # bot.edit_message_text(f"You selected {result}",
        #                       c.message.chat.id,
        #                       c.message.message_id)
        bot.delete_message(int(c.message.chat.id), c.message.message_id)

        if dt.date.today() > result:
            bot.send_message(c.message.chat.id, 'Дату из прошлого выбирать нельзя')
            check_in_out(c.message)
        elif get_user_table_db(c.message.chat.id)[8] == 'None':
            adding_values_db(c.message.chat.id, result, param='check_in')
            bot.send_message(c.message.chat.id, 'Выберите дату отъезда')
            check_in_out(c.message)
        elif get_user_table_db(c.message.chat.id)[9] == 'None':
            adding_values_db(c.message.chat.id, result, param='check_out')
            if get_user_table_db(c.message.chat.id)[-3] == '/bestdeal':
                get_size_price(c.message)
            else:
                get_city_count(c.message)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)