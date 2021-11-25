import requests
import json

from config import headers, url_detail
from classHotel import *
from botrequests.get_photos import get_photos
from logging_module import *


@logger.catch
@logging_decorator_responce
def get_best_hotels(query_param: dict, count_photos=0) -> list:
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
        'currency': query_param['currency'],
        'priceMin': query_param['priceMin'],
        'priceMax': query_param['priceMax'],
        'landmarkIds': float(query_param['landmarkIds'])
    }
    response = json.loads(requests.request('GET', url_detail, headers=headers, params=querystring_detail).text)
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
                                 cite=f'https://hotels.com/ho{hotel.get("id")}/?q-check-in={query_param["check_in"]}&q-check-out='
                                      f'{query_param["check_out"]}&q-rooms=1&q-room-0-adults=1&q-room-0-children=0',
                                 cite_for_db=f'https://hotels.com/search.do?destination-id={city_id}&q-check-in={query_param["check_in"]}'
                                             f'&q-check-out{query_param["check_out"]}&q-rooms=1&q-room-0-adults=2&q-room-0-children=0'
                                             f'&sort-order={querystring_detail["sortOrder"]}',
                                 user_id=query_param['user_id']
                                 ))
    return list_hotels
