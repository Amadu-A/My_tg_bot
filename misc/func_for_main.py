from telebot import types
import re
import itertools
from db.sqdb import *


def processing_admin(ADMIN_ID):
    """Отправление сообщения админу для функции send_to_admin"""
    processing_user_db(int(ADMIN_ID[0]))
    set_keys_false_db()
    set_keys_true_db()
    adding_language_into_languages_db(param='en')
    if str(get_user_table_db(ADMIN_ID[0])[-1]).isdigit() or get_user_table_db(ADMIN_ID[0])[-1] is None:
        value = 'en_US'
        adding_values_db(ADMIN_ID[0], value, param='locale')
    if get_user_table_db(ADMIN_ID[0])[-2] is None:
        cur_value = 'USD'
        adding_values_db(ADMIN_ID[0], cur_value, param='currency')


def set_locale_new_user(message_chat_id):
    """Функция, задающая язык и валюту для нового пользователя"""
    if str(get_user_table_db(message_chat_id)[-1]).isdigit() or get_user_table_db(message_chat_id)[-1] is None:
        value = 'en_US'
        adding_values_db(message_chat_id, value, param='locale')
    if get_user_table_db(message_chat_id)[-2] is None:
        cur_value = 'USD'
        adding_values_db(message_chat_id, cur_value, param='currency')


def main_commands(message_chat_id, message_text):
    """Обработка команд, заполнение словаря для функции welcome"""
    adding_user_id_db(id=message_chat_id)
    adding_values_db(message_chat_id, value=message_text, param='command')
    set_locale_new_user(message_chat_id)
    value = get_user_table_db(message_chat_id)
    for param in ['check_in', 'check_out', 'priceMin', 'priceMax','landmarkIds']:
        adding_values_db(message_chat_id, None, param=param)

    query_param = {
        'count_hotels': None,
        'city': None,
        'sorting': None,
        'destinationId': None,
        'best': None,
        'currency': value[-2],
        'locale': value[-1]
    }
    if message_text == '/lowprice':
        query_param['sorting'] = 'PRICE'
    elif message_text == '/highprice':
        query_param['sorting'] = 'PRICE_HIGHEST_FIRST'
    elif message_text == '/bestdeal':
        query_param['sorting'] = 'DISTANCE_FROM_LANDMARK'
    adding_values_db(message_chat_id, query_param['sorting'], param='sorting')
    return query_param


def processing_size_price(message_chat_id, message_text):
    """Функция для обработки ценового диапазона в команде /bestdeal для функции check_get_size_price"""
    result = re.findall(r'\d*', message_text)
    result = [int(size) for size in result if size.isdigit()]
    if len(result) != 2:
        raise Exception
    priceMin = min(int(result[0]), int(result[1]))
    priceMax = max(int(result[0]), int(result[1]))
    if priceMin < 0 or priceMax <= 0:
        raise Exception
    adding_values_db(message_chat_id, priceMin, param='priceMin')
    adding_values_db(message_chat_id, priceMax, param='priceMax')


def inline_settings(message_chat_id):
    """Формирование инлайн-клавиатуры для функции settings по обработке команды /settings"""
    adding_user_id_db(id=message_chat_id)
    set_locale_new_user(message_chat_id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('en', callback_data='en_US')
    item2 = types.InlineKeyboardButton('ru', callback_data='ru_RU')
    text1 = get_translated_item_db(message_chat_id, language=get_user_table_db(message_chat_id)[-1][:2], param='bot_6')
    item3 = types.InlineKeyboardButton(text1, callback_data='another_language')
    markup.add(item1, item2, item3)
    text = get_translated_item_db(message_chat_id, language=get_user_table_db(message_chat_id)[-1][:2], param='bot_4')

    markup2 = types.InlineKeyboardMarkup(row_width=2)
    item4 = types.InlineKeyboardButton('USD', callback_data='USD')
    item5 = types.InlineKeyboardButton('EUR', callback_data='EUR')
    item6 = types.InlineKeyboardButton('RUB', callback_data='RUB')
    item7 = types.InlineKeyboardButton(text1, callback_data='another_currency')
    markup2.add(item4, item5, item6, item7)
    text2 = get_translated_item_db(message_chat_id, language=get_user_table_db(message_chat_id)[-1][:2], param='bot_5')
    return text, markup, text2, markup2

def inline_photo_cnt():
    """Формирование инлайн-клавиатуры с выбором количества фото для функции callback_inline"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('1', callback_data=1)
    item2 = types.InlineKeyboardButton('3', callback_data=3)
    item3 = types.InlineKeyboardButton('5', callback_data=5)
    markup.add(item1, item2, item3)
    return markup


def new_number(id: int, count) -> int:
    id += 1
    if id > count:
        id = 1
    return id


