from botrequests.settings import translate_google
from db.sqdb import get_translated_item_db, get_user_table_db


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
        text1 = get_translated_item_db(language=get_user_table_db(self.user_id)[-1][:2], param='msg_1')
        text2 = get_translated_item_db(language=get_user_table_db(self.user_id)[-1][:2], param='msg_2')
        text3 = get_translated_item_db(language=get_user_table_db(self.user_id)[-1][:2], param='msg_3')
        text4 = get_translated_item_db(language=get_user_table_db(self.user_id)[-1][:2], param='msg_4')
        text5 = get_translated_item_db(language=get_user_table_db(self.user_id)[-1][:2], param='msg_5')
        text6 = get_translated_item_db(language=get_user_table_db(self.user_id)[-1][:2], param='msg_6')

        message = f'{self.name}\n\n' \
                  f'{text1} {"☆" * int(self.star_rating)}\n' \
                  f'{text2} {self.price}\n' \
                  f'{text3} {self.postal_code}\n' \
                  f'{text4} {self.country}, {self.city}, {self.address}\n' \
                  f'{self.distance} {text5}\n' \
                  f'{text6} {self.cite}\n'
        return message
