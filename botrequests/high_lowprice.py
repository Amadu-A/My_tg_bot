import requests
import json
from requests.exceptions import Timeout
from typing import Union

from config import headers, url_id_city, url_detail #rotate_RAPIDAPI_KEY
from botrequests.get_photos import get_photos
from misc.classHotel import *
from misc.logging_module import *


@logger.catch
@logging_decorator_responce
def get_city_list(city_name: str, query_param: dict) -> Union[dict, str]:
    """
    Функция парсит город с сайта api Hotels и возвращает словарь с результатом
    :param city_name: str
    :param query_param: dict
    :return: dict
    """
    try:
        querystring_search = {'query': city_name.title(), 'locale': query_param['locale'],
                              'currency': query_param['currency']}
        response = requests.request('GET', url_id_city, headers=headers, params=querystring_search, timeout=10)
        return response.json()['suggestions'][0]['entities']
    except Timeout:
        return 'Время ожидания ответа истекло'                 # TODO

@logger.catch
@logging_decorator_responce
def get_hotels(query_param: dict, count_photos: int = 0) -> Union[list, str]:
    """
    Функция парсит сайт api Hotels с заданными параметрами и возвращает список инстансов Hotel с отелями
    :param query_param: dict
    :param count_photos: int
    :return: list
    """
    city_id = query_param['destinationId']
    querystring_detail = {
        'adults1': '1',
        'pageNumber': '1',
        'destinationId': city_id,
        'pageSize': str(query_param['count_hotels']),
        'checkOut': query_param['check_out'],
        'checkIn': query_param['check_in'],
        'sortOrder': query_param['sorting'],
        'locale': query_param['locale'],
        'currency': query_param['currency']
    }
    try:
        response = requests.request('GET', url_detail, headers=headers, params=querystring_detail, timeout=10)
        response = json.loads(response.text)
        if 'You have exceeded' in str(response.get('message')) or 'Upgrade your plan at' in str(response.get('message')):
            raise Exception
        result = response.get('data').get('body').get('searchResults').get('results')
        list_hotels = []
        for hotel in result:
            list_hotels.append(Hotel(hotel_id=hotel.get('id'),
                                     name=hotel.get('name'),
                                     country=hotel.get('address').get('countryName'),
                                     city=hotel.get('address').get('locality'),
                                     postal_code=hotel.get('address').get('postalCode'),
                                     address=hotel.get('address').get('streetAddress'),
                                     star_rating=hotel.get('starRating'),
                                     distance=hotel.get("landmarks")[0].get('distance'),
                                     price=hotel.get('ratePlan').get('price').get('current'),
                                     photo_path_list=get_photos(hotel.get('id'), count_photos),
                                     cite=f'https://hotels.com/ho{hotel.get("id")}/?q-check-in='
                                          f'{query_param["check_in"]}&q-check-out='
                                          f'{query_param["check_out"]}&q-rooms=1&q-room-0-adults=1&q-room-0-children=0',
                                     cite_for_db=f'https://hotels.com/search.do?destination-id={city_id}'
                                                 f'&q-check-in={query_param["check_in"]}'
                                                 f'&q-check-out{query_param["check_out"]}'
                                                 f'&q-rooms=1&q-room-0-adults=2&q-room-0-children=0'
                                                 f'&sort-order={querystring_detail["sortOrder"]}',
                                     user_id=query_param['user_id']
                                     ))
        return list_hotels
    except Timeout:
        return 'Время ожидания истекло'

