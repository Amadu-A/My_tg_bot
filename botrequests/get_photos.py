import requests
import json

from config import headers, url_photos


def get_photos(hotel_id: int, count_photo: int) -> list:
    """
    Функция парсит фотографии с сайта api Hotels и возвращает список с результатом
    :param hotel_id: int
    :param count_photo: int
    :return: list
    """
    if count_photo == 0:
        return []
    responce = json.loads(requests.request("GET", url_photos, headers=headers, params={'id': str(hotel_id)}).text)
    if len(responce.get('hotelImages')) > count_photo:
        responce = (responce.get('hotelImages'))[:count_photo]
    else:
        responce = responce.get('hotelImages')
    photo_path_list = [item.get('baseUrl').format(size='z') for item in responce]
    return photo_path_list
