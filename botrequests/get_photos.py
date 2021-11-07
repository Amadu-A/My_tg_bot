import requests
import json

from config import headers, url_photos


def get_photos(hotel_id: int, count_photo: int) -> list:
    print('нормальный код', count_photo)
    if count_photo == 0:
        return []
    print('плохой  код1', count_photo)
    responce = json.loads(requests.request("GET", url_photos, headers=headers, params={'id': str(hotel_id)}).text)
    if len(responce.get('hotelImages')) > count_photo:
        responce = (responce.get('hotelImages'))[:count_photo]
    else:
        print('плохой  код2', count_photo)
        responce = responce.get('hotelImages')
    print('плохой  код3', count_photo)
    photo_path_list = [item.get('baseUrl').format(size='z') for item in responce]
    return photo_path_list
