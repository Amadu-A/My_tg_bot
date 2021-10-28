class User:
    def __init__(self, user_id=None, query_param: dict=None):
        self.user_id = user_id
        self.query_param = {
                    'count_hotels': None,
                    'city': None,
                    'sorting': 'PRICE',
                    'locale': 'en_US',
                    'destinationId': None
        }
    def __str__(self):
        return self.user_id


class Hotel:
    def __init__(self, hotel_id=None,
                 name=None,
                 country=None,
                 city=None,
                 postal_code=None,
                 address=None,
                 star_rating=None,
                 distance=None,
                 price=None,
                 photo_path_list=None,
                 cite=None):
        self.hotel_id = hotel_id
        self.name = name
        self.country = country
        self.city = city
        self.postal_code = postal_code
        self.address = address
        self.star_rating = star_rating
        self.distance = distance
        self.price = price
        self.photo_path_list = photo_path_list
        self.cite = cite

    def get_hotel(self):
        message = f'{self.name}\n\n' \
                  f'Рейтинг "☆" {self.star_rating}\n' \
                  f'Адрес {self.country}, {self.city}, {self.address}\n' \
                  f'Индекс {self.postal_code}\n' \
                  f'Сайт {self.cite}\n' \
                  f'{self.distance} км от центра города\n' \
                  f'Цена за сутки за 1 человека {self.price}\n'
        return message
# f'Рейтинг "☆" * {int(self.star_rating)}\n' \



