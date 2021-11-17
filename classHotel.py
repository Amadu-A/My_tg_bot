from botrequests.settings import translate_google


class Hotel:
    """
    Класс для хранения параметров по каждому отелю
    """
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
                 cite=None,
                 cite_for_db=None,
                 user_id=None):
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
        self.cite_for_db = cite_for_db
        self.user_id = user_id

    def get_hotel(self) -> str:
        """
        Метод для формирования сообщения, которое будет отправляться пользователю бота с результатами запроса
        :return: str
        """
        text1 = translate_google('Рейтинг', self.user_id)
        text2 = translate_google('Цена за выбранный период за 1 человека', self.user_id)
        text3 = translate_google('Индекс', self.user_id)
        text4 = translate_google('Адрес', self.user_id)
        text5 = translate_google('от центра города', self.user_id)
        text6 = translate_google('Сайт', self.user_id)

        message = f'{self.name}\n\n' \
                  f'{text1} {"☆" * int(self.star_rating)}\n' \
                  f'{text2} {self.price}\n' \
                  f'{text3} {self.postal_code}\n' \
                  f'{text4} {self.country}, {self.city}, {self.address}\n' \
                  f'{self.distance} {text5}\n' \
                  f'{text6} {self.cite}\n'
        return message
