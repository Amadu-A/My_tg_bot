import requests
import json
import re

from config import headers, date_today, date_tomorrow, url_id_city, url_detail
from botrequests.get_photos import get_photos
from classHotel import *


def get_city_list(city_name: str, query_param: dict):
    querystring_search = {'query': city_name.title(), 'locale': query_param['locale'], 'currency': query_param['currency']}
    print('11 строка hi-low-price:', querystring_search)
    # if re.search(r'[A-Za-z]', city_name):
    #     querystring_search['locale'] = 'en_US' # TODO надо изменить
    response = requests.request('GET', url_id_city, headers=headers, params=querystring_search)
    print(response)
    print('**********')
    #print(response.text)
    #print(json.dumps(response.json(), indent=4))
    print('**********'*2)
    #print(json.dumps(response.json()['suggestions'][0]['entities'], indent=4))

    return response.json()['suggestions'][0]['entities']

def get_hotels(query_param: dict, count_photos=0):
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
    print(querystring_detail)
    response = json.loads(requests.request('GET', url_detail, headers=headers, params=querystring_detail).text)
    print(response)
    result = response.get('data').get('body').get('searchResults').get('results')
    print(json.dumps(result, indent=4))
    list_hotels = []
    print('кол фото', count_photos)
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
                                #cite=f'https://ru.hotels.com/ho{hotel.get("id")}',
                                cite=f'https://hotels.com/ho{hotel.get("id")}/?q-check-in={query_param["check_in"]}&q-check-out='
                                     f'{query_param["check_out"]}&q-rooms=1&q-room-0-adults=1&q-room-0-children=0',
                                cite_for_db=f'https://hotels.com/search.do?destination-id={city_id}&q-check-in={query_param["check_in"]}'
                                     f'&q-check-out{query_param["check_out"]}&q-rooms=1&q-room-0-adults=2&q-room-0-children=0'
                                     f'&sort-order={querystring_detail["sortOrder"]}',
                                user_id=query_param['user_id']
        ))
    return list_hotels


# cite = f'https://hotels.com/search.do?destination-id={city_id}&q-check-in={date_today}'
# f'&q-check-out{date_tomorrow}&q-rooms=1&q-room-0-adults=2&q-room-0-children=0'
# f'&sort-order={querystring_detail["sortOrder"]}',

#round(float(('.').join(hotel.get("landmarks")[0].get('distance').split(' ')[0].split(','))) * 1.6093, 2)