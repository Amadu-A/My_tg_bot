import telebot
from telebot import types
from telebot.types import InputMediaPhoto
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import datetime as dt
import re

from config import BOT_TOKEN, ADMIN_ID
from botrequests.high_lowprice import get_city_list, get_hotels
from botrequests.settings import get_list_locale, choose_currency
from botrequests.bestdeal import get_best_hotels
from db.sqdb import *
from misc.logging_module import *
from misc.func_for_main import processing_admin, set_locale_new_user, main_commands, processing_size_price, \
    inline_photo_cnt, inline_settings


bot = telebot.TeleBot(BOT_TOKEN, parse_mode='html')


@logger.catch
@logging_decorator
def send_to_admin(ADMIN_ID) -> None:
    """
    Сообщение админу о запуске бота, выставление настроек по умолчанию, создание таблиц базы данных
    :param ADMIN_ID: lst[str]
    """
    bot.send_message(ADMIN_ID[0], text='Бот запущен!')
    processing_admin(ADMIN_ID)


@logger.catch
@logging_decorator
@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def welcome(message: types.Message) -> None:
    """Функция, обрабатывающая команды '/lowprice', '/highprice', '/bestdeal'"""
    query_param = main_commands(message.chat.id, message.text)
    text = get_translated_item_db(message.chat.id, language=get_user_table_db(message.chat.id)[-1][:2], param='bot_7')
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, callback=keyboard_city, query_param=query_param)


@logger.catch
@logging_decorator
@bot.message_handler(commands=['settings'])
def settings(message: types.Message) -> None:
    """Функция для обработки команды /settings. Формирует удобную инлайн-клавиатуру с распространенными
    языками и валютами, а также предлагает сформировать клавиатуру со всеми остальными вариантами"""
    text, markup, text2, markup2 = inline_settings(message.chat.id)
    bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.send_message(message.chat.id, text2, reply_markup=markup2)


@logger.catch
@logging_decorator
@bot.callback_query_handler(
    func=lambda call: (len(call.data) == 5 and call.data[2] == '_') or str(call.data) in choose_currency())
def callback_inline(call: types.CallbackQuery) -> None:
    """
    Хендлер для инлайн-клавиатуры. Отлавливает значение callback_data: Выбор языка / Выбор валюты
    :param call: types.CallbackQuery
    """
    bot.delete_message(int(call.message.chat.id), call.message.message_id)
    if str(call.data) in choose_currency():
        adding_values_db(call.message.chat.id, str(call.data), param='currency')
    else:
        adding_values_db(call.message.chat.id, call.data, param='locale')
        adding_language_into_languages_db(param=call.data[:2])


@logger.catch
@logging_decorator
@bot.callback_query_handler(
    func=lambda call: str(call.data) == 'another_language' or str(call.data) == 'another_currency')
def callback_inline(call: types.CallbackQuery) -> None:
    """
    Хендлер для инлайн-клавиатуры. Отлавливает события в соответствии со значением callback_data:
    Выбор языка или валюты из списка доступных. Составление инлайн-кнопок по выбору языка и валюты
    :param call: 'another_language' / 'another_currency'
    """
    param = call.data
    bot.delete_message(int(call.message.chat.id), call.message.message_id)
    if param == 'another_language':
        markup = types.InlineKeyboardMarkup(row_width=2)
        for key, val in get_list_locale().items():
            item = types.InlineKeyboardButton(key, callback_data=val)
            markup.add(item)
        text = get_translated_item_db(call.message.chat.id, language=get_user_table_db(call.message.chat.id)[-1][:2],
                                      param='bot_4')
        bot.send_message(call.message.chat.id, text=text, reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        for elem in choose_currency():
            item = types.InlineKeyboardButton(elem, callback_data=elem)
            markup.add(item)
        text = get_translated_item_db(call.message.chat.id, language=get_user_table_db(call.message.chat.id)[-1][:2],
                                      param='bot_5')
        bot.send_message(call.message.chat.id, text=text, reply_markup=markup)


@logger.catch
@logging_decorator
@bot.message_handler(commands=['history'])
def history(message: types.Message) -> None:
    """Функция, обрабатывающая команду '/history'"""
    set_locale_new_user(message.chat.id)
    data_order = get_data_order_db(message.chat.id)
    if data_order[-1][-1] == 'История пуста':
        text = get_translated_item_db(message.chat.id, language=get_user_table_db(message.chat.id)[-1][:2],
                                      param='bot_21')
        bot.send_message(chat_id=message.chat.id, text=text)
    else:
        for response in data_order:
            text = get_translated_item_db(message.chat.id, language=get_user_table_db(message.chat.id)[-1][:2],
                                          param='bot_1') + response[-4] \
                   + '\n' + get_translated_item_db(message.chat.id, language=get_user_table_db(message.chat.id)[-1][:2],
                                                   param='bot_2') \
                   + response[-3] + '\n' + get_translated_item_db(message.chat.id,
                                                                  language=get_user_table_db(message.chat.id)[-1][:2],
                                                                  param='bot_3') \
                   + response[-2] + '\n' + response[-1]
            bot.send_message(chat_id=message.chat.id, text=text)


@logger.catch
@logging_decorator
@bot.message_handler(commands=['clear_history'])
def history(message: types.Message) -> None:
    """Функция, обрабатывающая команду '/clear_history'"""
    set_locale_new_user(message.chat.id)
    clear_history(int(message.chat.id))
    text = get_translated_item_db(message.chat.id, language=get_user_table_db(message.chat.id)[-1][:2], param='bot_21')
    bot.send_message(chat_id=message.chat.id, text=text)


@logger.catch
@logging_decorator
@bot.message_handler(content_types=['text'])
def get_textmessages(message: types.Message) -> None:
    """Функция, помогающая выбрать нужную команду, реагирует на любой текст, не являющийся командой"""
    processing_user_db(message.chat.id)
    set_locale_new_user(message.chat.id)
    text = []
    for count in range(1, 8):
        text.append(get_translated_item_db(message.chat.id, language=get_user_table_db(message.chat.id)[-1][:2],
                                   param='command_' + str(count)))
    help_msg = "/lowprice - {}\n/highprice - {}\n/bestdeal - {}\n/history - {}\n/clear_history - {}" \
               "\n/settings - {}\n{} hotels.com\nThis is a self-learning bot. If you change the language, " \
               "but it's still Russian, change it to English".format(text[0], text[1], text[2], text[3], text[6],
                                                                     text[4], text[5])
    bot.send_message(message.from_user.id, text=help_msg)


@logger.catch
@logging_decorator
def keyboard_city(message: types.Message, query_param: dict) -> None:
    """Клавиатура с вариантами городов"""
    city = message.text.lower()
    data = get_city_list(city, query_param)
    if isinstance(data, str):
        msg = bot.send_message(message.chat.id, text=data)                        # TODO
        bot.register_next_step_handler(message=msg, callback=keyboard_city, query_param=query_param)
    else:
        kb_cities = types.InlineKeyboardMarkup(row_width=1)
        for elem in data:
            #elem['name'] = ''.join(list(map(lambda x: x if (x.isalpha() or x == '-') else ' ', elem['name'])))[:25]
            new_btn = types.InlineKeyboardButton(text=elem['name'] + ',' + elem['caption'].split(',')[-1],
                                                 callback_data=f"{elem['destinationId']}+{elem['name'][:25]}")
            kb_cities.add(new_btn)
        if len(kb_cities.to_dict()['inline_keyboard']) == 0:
            text = get_translated_item_db(message.chat.id, language=get_user_table_db(message.chat.id)[-1][:2],
                                          param='bot_8') + ' ' + city.title() + ' ' \
                   + get_translated_item_db(message.chat.id, language=get_user_table_db(message.chat.id)[-1][:2],
                                            param='bot_9')
            msg = bot.send_message(message.chat.id, text)
            bot.register_next_step_handler(message=msg, callback=keyboard_city, query_param=query_param)
        else:
            text = get_translated_item_db(message.chat.id, language=get_user_table_db(message.chat.id)[-1][:2],
                                          param='bot_10')
            bot.send_message(message.from_user.id, reply_markup=kb_cities,
                             text=text, parse_mode='html')


@logger.catch
@logging_decorator
@bot.callback_query_handler(func=lambda call: '+' in str(call.data))
def callback_inline(call: types.CallbackQuery) -> None:
    """
    Хендлер для инлайн-клавиатуры. Отлавливает значение callback_data: id города и имя города
    """
    bot.delete_message(int(call.message.chat.id), call.message.message_id)
    value = call.data.split('+')
    processing_user_db(call.message.chat.id)
    adding_values_db(call.message.chat.id, value[0], param='destinationId')
    adding_values_db(call.message.chat.id, value[1], param='city')
    text = get_translated_item_db(call.message.chat.id, language=get_user_table_db(call.message.chat.id)[-1][:2],
                                  param='bot_18')
    bot.send_message(call.message.chat.id, text)
    check_in_out(call.message)


@logger.catch
@logging_decorator
def get_city_count(message: types.Message) -> None:
    """Клавиатура с выбором количества отелей"""
    markup = types.InlineKeyboardMarkup(row_width=3)
    item1 = types.InlineKeyboardButton('5', callback_data='6')
    item2 = types.InlineKeyboardButton('10', callback_data='11')
    #item3 = types.InlineKeyboardButton('25', callback_data='26')
    markup.add(item1, item2)
    text = get_translated_item_db(message.chat.id, language=get_user_table_db(message.chat.id)[-1][:2], param='bot_11')
    bot.send_message(message.chat.id, text, reply_markup=markup)


@logger.catch
@logging_decorator
@bot.callback_query_handler(func=lambda call: len(str(call.data)) < 3 and int(call.data) > 5)
def callback_inline(call: types.CallbackQuery) -> None:
    """
    Хендлер для инлайн-клавиатуры. Отлавливает значение callback_data: Количество отелей
    """
    bot.delete_message(int(call.message.chat.id), call.message.message_id)
    count_hotels = int(call.data) - 1
    adding_values_db(call.message.chat.id, count_hotels, param='count_hotels')
    print_photo(call.message)


@logger.catch
@logging_decorator
def get_size_price(message: types.Message) -> None:
    """Функция для указания ценового диапазона в команде /bestdeal"""
    text = get_translated_item_db(message.chat.id, language=get_user_table_db(message.chat.id)[-1][:2], param='bot_12')
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, callback=check_get_size_price)


@logger.catch
@logging_decorator
def check_get_size_price(message: types.Message) -> None:
    """Функция для обработки ценового диапазона в команде /bestdeal"""
    try:
        processing_size_price(message.chat.id, message.text)
        get_distance(message)
    except (TypeError, IndexError, Exception):
        get_size_price(message)


@logger.catch
@logging_decorator
def get_distance(message: types.Message) -> None:
    """Функция для указания параметра удаленности в команде /bestdeal"""
    text = get_translated_item_db(message.chat.id, language=get_user_table_db(message.chat.id)[-1][:2], param='bot_13')
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, callback=check_get_distance)


@logger.catch
@logging_decorator
def check_get_distance(message: types.Message) -> None:
    """Функция для обработки параметра удаленности в команде /bestdeal"""
    try:
        landmarkIds = round(float(re.sub(r'[.,\s]', '.', message.text)), 2)
        adding_values_db(message.chat.id, landmarkIds, param='landmarkIds')
        get_city_count(message)
    except ValueError:
        get_distance(message)


@logger.catch
@logging_decorator
def print_photo(message: types.Message) -> None:
    """Функция с клавиатурой выбора вывода фотографий отелей"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('✔', callback_data='yes')
    item2 = types.InlineKeyboardButton('✘', callback_data='none')
    markup.add(item1, item2)
    text = get_translated_item_db(message.chat.id, language=get_user_table_db(message.chat.id)[-1][:2], param='bot_14')
    bot.send_message(message.chat.id, text, reply_markup=markup)


@logger.catch
@logging_decorator
@bot.callback_query_handler(func=lambda call: str(call.data) == 'yes')
def callback_inline(call: types.CallbackQuery) -> None:
    """
    Хендлер для инлайн-клавиатуры. Формирует инл-клавиатуру с выбором количества фото
    :param call: Положительный ответ на вопрос о печати фото
    """
    bot.delete_message(int(call.message.chat.id), call.message.message_id)
    markup = inline_photo_cnt()
    text = get_translated_item_db(call.message.chat.id, language=get_user_table_db(call.message.chat.id)[-1][:2],
                                  param='bot_15')
    bot.send_message(call.message.chat.id, text, reply_markup=markup)


@logger.catch
@logging_decorator
@bot.callback_query_handler(func=lambda call: str(call.data) == 'none' or
                                              (str(call.data).isdigit() and len(call.data) == 1))
def callback_inline(call: types.CallbackQuery) -> None:
    """
    Хендлер для инлайн-клавиатуры. Отлавливает события в соответствии со значением callback_data
    :param call: Отрицательный ответ на печать фото, либо callback c количеством фото
    """
    bot.delete_message(int(call.message.chat.id), call.message.message_id)
    text = get_translated_item_db(call.message.chat.id, language=get_user_table_db(call.message.chat.id)[-1][:2],
                                  param='bot_16')
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
    if isinstance(hotels_lst, str):
        bot.send_message(call.message.chat.id, text=hotels_lst)                                    # TODO
    elif not len(hotels_lst):
        text = get_translated_item_db(call.message.chat.id, language=get_user_table_db(call.message.chat.id)[-1][:2],
                                      param='bot_22')
        bot.send_message(call.message.chat.id, text=text)
    else:
        for hotel in hotels_lst:
            bot.send_message(chat_id=call.message.chat.id, text=hotel.get_hotel(), disable_web_page_preview=True)
            data += hotel.get_hotel() + '\n'
            if count_photos > 0:
                try:
                    bot.send_media_group(chat_id=call.message.chat.id,
                                         media=[InputMediaPhoto(media=path) for path in hotel.photo_path_list])
                except (Exception):
                    for path in hotel.photo_path_list:
                        try:
                            print(path)
                            bot.send_photo(chat_id=call.message.chat.id, photo=path)
                        except Exception:
                            continue
        if get_maxorder_db(call.message.chat.id) != None:
            order_id = get_maxorder_db(call.message.chat.id) + 1
        adding_orders_db(id_order=order_id,
                         id_user=call.message.chat.id,
                         date=str(dt.datetime.now()),
                         command=get_user_table_db(call.message.chat.id)[-3],
                         cite=hotel.cite_for_db,
                         value=data)


@logger.catch
@logging_decorator
def check_in_out(message: types.Message) -> None:
    """Функция для формирующая инлайн-календарь"""
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)


@logger.catch
@logging_decorator
@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c: types.CallbackQuery) -> None:
    """Функция для выбора даты через инлайн-календарь"""
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        res = dt.datetime.strptime(str(result), "%Y-%m-%d")
        bot.delete_message(int(c.message.chat.id), c.message.message_id)
        if dt.date.today() > result:
            text = get_translated_item_db(c.message.chat.id, language=get_user_table_db(c.message.chat.id)[-1][:2],
                                          param='bot_19')
            bot.send_message(c.message.chat.id, text)
            check_in_out(c.message)
        elif get_user_table_db(c.message.chat.id)[8] == 'None':
            adding_values_db(c.message.chat.id, result, param='check_in')
            text = get_translated_item_db(c.message.chat.id, language=get_user_table_db(c.message.chat.id)[-1][:2],
                                          param='bot_20')
            bot.send_message(c.message.chat.id, text)
            check_in_out(c.message)
        elif get_user_table_db(c.message.chat.id)[9] == 'None' and dt.datetime.strptime(
                str(get_user_table_db(c.message.chat.id)[8]), "%Y-%m-%d") < res:
            adding_values_db(c.message.chat.id, result, param='check_out')
            if get_user_table_db(c.message.chat.id)[-3] == '/bestdeal':
                get_size_price(c.message)
            else:
                get_city_count(c.message)
        else:
            text = get_translated_item_db(c.message.chat.id, language=get_user_table_db(c.message.chat.id)[-1][:2],
                                          param='bot_20')
            bot.send_message(c.message.chat.id, text)
            check_in_out(c.message)


if __name__ == '__main__':
    send_to_admin(ADMIN_ID)
    bot.polling(none_stop=True, interval=0)
