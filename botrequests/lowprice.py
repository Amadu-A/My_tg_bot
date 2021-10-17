import requests
import json

from main import headers, date_today, date_tomorrow
from classUser import *


url_id_city = 'https://hotels4.p.rapidapi.com/locations/search'
url_detail = 'https://hotels4.p.rapidapi.com/properties/list'
url_lang = 'https://hotels4.p.rapidapi.com/get-meta-data'


# def get_hotels(query_param: dict):
#     querystring_search = {'query': query_param['city'], 'locale': 're_RU'}
#     response = json.loads(requests.request('GET', url_id_city, headers=headers, params=querystring_search).text)
#     print(response)
#     city_id = response.get('suggestions')[0].get('entities')[0].get('destinationId')
#     querystring_detail = {
#         'adults1': '1',
#         'pageNumber': '1',
#         'destinationId': city_id,
#         'pageSize': str(query_param['count_hotels']),
#         'checkOut': '{}'.format(date_tomorrow),
#         'checkIn': '{}'.format(date_today),
#         'sortOrder': query_param['sorting'],
#         'locale': 'ru_RU',
#         'currency': 'RUB'
#     }
#     print(querystring_detail)
#     response = json.loads(requests.request('GET', url_detail, headers=headers, params=querystring_detail).text)
#     print(response)
#     result = response.get('data').get('body').get('searchResults').get('results')
#     print(json.dumps(result, indent=4))
#     list_hotels = []
#     for hotel in result:
#         list_hotels.append(User(hotel_id=hotel.get('id'),
#                                 name=hotel.get('name'),
#                                 country=hotel.get('address').get('countryName'),
#                                 city=hotel.get('address').get('locality'),
#                                 postal_code=hotel.get('address').get('postalCode'),
#                                 address=hotel.get('address').get('streetAddress'),
#                                 star_rating=hotel.get('star_rating'),
#                                 #distance=hotel.get('distance'),
#                                 price=hotel.get('ratePlan').get('price').get('current')
#                                 # место для фото
#                                 #cite=hotel.get('cite')
#         ))
#     return list_hotels

