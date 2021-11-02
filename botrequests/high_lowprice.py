import requests
import json
import re

from config import headers, date_today, date_tomorrow, url_id_city, url_detail
from classHotel import *


def get_city_list(city_name: str, query_param: dict):
    querystring_search = {'query': city_name.title(), 'locale': query_param['locale']}
    print('11 строка hi-low-price:', querystring_search)
    if re.search(r'[A-Za-z]', city_name):
        querystring_search['locale'] = 'en_US' # TODO надо изменить
    response = requests.request('GET', url_id_city, headers=headers, params=querystring_search)

    print('**********')
    #print(json.dumps(response.json(), indent=4))
    print('**********'*2)
    print(json.dumps(response.json()['suggestions'][0]['entities'], indent=4))

    return response.json()['suggestions'][0]['entities']

def get_hotels(query_param: dict):
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
        'currency': query_param['currency']       # TODO надо изменить
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
                                distance=round(float(hotel.get("landmarks")[0].get('distance').split(' ')[0]) * 1.6093, 2),
                                price=hotel.get('ratePlan').get('price').get('current'),
                                # место для фото
                                cite=f'https://hotels.com/search.do?destination-id={city_id}&q-check-in={date_today}'
                                     f'&q-check-out{date_tomorrow}&q-rooms=1&q-room-0-adults=2&q-room-0-children=0'
                                     f'&sort-order={querystring_detail["sortOrder"]}'
        ))
    return list_hotels

