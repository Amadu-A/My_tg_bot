import requests
import json
from requests.exceptions import Timeout
from typing import Union

from config import headers, url_photos # rotate_RAPIDAPI_KEY


def get_photos(hotel_id: int, count_photo: int)-> Union[list, str]:
    """
    Функция парсит фотографии с сайта api Hotels и возвращает список с результатом
    :param hotel_id: int
    :param count_photo: int
    :return: Union[list, str]
    """
    if count_photo == 0:
        return []
    else:
        try:
            response = json.loads(requests.request("GET",
                                                   url_photos,
                                                   headers=headers,
                                                   params={'id': str(hotel_id)},
                                                   timeout=10).text)
            if 'You have exceeded' in str(response.get('message')) or 'Upgrade your plan at' in str(response.get('message')):
                raise BaseException
            if len(response.get('hotelImages')) > count_photo:
                response = (response.get('hotelImages'))[:count_photo]
            else:
                response = response.get('hotelImages')
            photo_path_list = [item.get('baseUrl').format(size='z') for item in response]
            return photo_path_list
        except Timeout:
            return 'Время ожидания истекло'  # TODO
        except BaseException('You have exceeded the MONTHLY quota for Requests on your current plan, BASIC. '
                             'Upgrade your plan at https://rapidapi.com/apidojo/api/hotels4'):
            #rotate_RAPIDAPI_KEY()
            #get_photos(hotel_id, count_photo)
            print('Поменять ключи')
