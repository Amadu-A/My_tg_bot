import requests
import json
import re

from config import headers, date_today, date_tomorrow, url_detail
from classHotel import *
from botrequests.get_photos import get_photos
from botrequests.settings import translate_google_converter


def get_best_hotels(query_param: dict, count_photos=0):
    city_id = query_param['destinationId']
    querystring_detail = {
        'adults1': '1',
        'pageNumber': '1',
        'destinationId': city_id,
        'pageSize': str(query_param['count_hotels']),
        'checkOut': '{}'.format(date_tomorrow),
        'checkIn': '{}'.format(date_today),
        'sortOrder': query_param['sorting'],
        'locale': query_param['locale'],
        'currency': query_param['currency'],
        'priceMin': query_param['priceMin'],
        'priceMax': query_param['priceMax'],
        'landmarkIds': float(query_param['landmarkIds'])
    }
    print(querystring_detail)
    response = json.loads(requests.request('GET', url_detail, headers=headers, params=querystring_detail).text)
    print(response)
    result = response.get('data').get('body').get('searchResults').get('results')
    print(json.dumps(result, indent=4))
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
                                cite=f'https://hotels.com/search.do?destination-id={city_id}&q-check-in={date_today}'
                                     f'&q-check-out{date_tomorrow}&q-rooms=1&q-room-0-adults=2&q-room-0-children=0'
                                     f'&sort-order={querystring_detail["sortOrder"]}'
        ))
    return list_hotels

# def converter(distance):
#     print(distance)
#     return round(float(('.').join(translate_google_converter(distance)).split(' ')[0].split(',')) * 1.6093, 2)

def get_foto(query_param: dict):
    pass